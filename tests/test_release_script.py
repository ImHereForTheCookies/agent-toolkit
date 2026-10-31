"""plugins/ticket-loop/scripts/release.sh against a throwaway repo with a local bare remote."""
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "plugins" / "ticket-loop" / "scripts" / "release.sh"
GIT_ENV = ["-c", "user.name=t", "-c", "user.email=t@t"]


def git(cwd, *args):
    return subprocess.run(["git", *GIT_ENV, *args], cwd=cwd, check=True,
                          capture_output=True, text=True).stdout.strip()


def make_repo(tmp_path, verify_ok=True):
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(remote)], check=True)
    work = tmp_path / "work"
    subprocess.run(["git", "init", "-q", "-b", "main", str(work)], check=True)
    poc = work / "pocs" / "demo"
    poc.mkdir(parents=True)
    rc = "true" if verify_ok else "false"
    (poc / "Makefile").write_text(
        f"setup:\n\t@true\nverify:\n\t@{rc}\nbuild:\n\t@mkdir -p dist\n")
    (poc / ".gitignore").write_text("dist/\n")
    (poc / "app.js").write_text("v1\n")
    (work / "root.txt").write_text("root\n")
    git(work, "add", "-A")
    git(work, "commit", "-qm", "init")
    git(work, "remote", "add", "origin", str(remote))
    git(work, "push", "-q", "origin", "main")
    return work, remote


def release(work, folder, slug):
    return subprocess.run(["bash", str(SCRIPT), str(work), folder, slug,
                           "--notes", str(work.parent / "notes.md")],
                          capture_output=True, text=True,
                          env={**os.environ, "RELEASE_SKIP_FETCH": "1",
                               "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                               "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})


def test_first_release_creates_version_branch_and_moves_branch(tmp_path):
    work, remote = make_repo(tmp_path)
    r = release(work, "pocs/demo", "demo")
    assert r.returncode == 0, r.stderr
    head = git(work, "rev-parse", "HEAD")
    assert git(remote, "rev-parse", "refs/heads/release/demo-v1") == head
    assert git(remote, "rev-parse", "refs/heads/release/demo") == head
    assert git(remote, "tag", "-l") == ""  # releases never push tags


def test_no_changes_means_nothing_to_release(tmp_path):
    work, _ = make_repo(tmp_path)
    assert release(work, "pocs/demo", "demo").returncode == 0
    (work / "root.txt").write_text("other project changed\n")
    git(work, "commit", "-qam", "unrelated")
    r = release(work, "pocs/demo", "demo")
    assert r.returncode == 3, r.stdout + r.stderr


def test_second_release_fast_forwards(tmp_path):
    work, remote = make_repo(tmp_path)
    release(work, "pocs/demo", "demo")
    (work / "pocs/demo/app.js").write_text("v2\n")
    git(work, "commit", "-qam", "feature two")
    r = release(work, "pocs/demo", "demo")
    assert r.returncode == 0, r.stderr
    head = git(work, "rev-parse", "HEAD")
    v1 = git(remote, "rev-parse", "refs/heads/release/demo-v1")
    assert v1 != head  # old versions stay where they were cut
    assert git(remote, "rev-parse", "refs/heads/release/demo-v2") == head
    assert git(remote, "rev-parse", "refs/heads/release/demo") == head
    assert "feature two" in r.stdout + (work.parent / "notes.md").read_text()


def test_failed_verify_cuts_nothing(tmp_path):
    work, remote = make_repo(tmp_path, verify_ok=False)
    r = release(work, "pocs/demo", "demo")
    assert r.returncode != 0
    assert git(remote, "branch", "--list", "release/*") == ""


def test_root_project_ignores_pocs_changes(tmp_path):
    work, _ = make_repo(tmp_path)
    (work / "Makefile").write_text("verify:\n\t@true\n")
    git(work, "add", "-A")
    git(work, "commit", "-qm", "root makefile")
    assert release(work, ".", "rootapp").returncode == 0
    (work / "pocs/demo/app.js").write_text("poc only\n")
    git(work, "commit", "-qam", "poc change")
    assert release(work, ".", "rootapp").returncode == 3


def test_repairs_release_branch_when_second_push_was_lost(tmp_path):
    work, remote = make_repo(tmp_path)
    release(work, "pocs/demo", "demo")
    head = git(work, "rev-parse", "HEAD")
    # Simulate a cut whose release/<slug> push failed after the version branch landed.
    (work / "pocs/demo/app.js").write_text("v2\n")
    git(work, "commit", "-qam", "feature two")
    v2 = git(work, "rev-parse", "HEAD")
    git(work, "push", "-q", "origin", f"{v2}:refs/heads/release/demo-v2")
    assert git(remote, "rev-parse", "refs/heads/release/demo") == head
    r = release(work, "pocs/demo", "demo")
    assert r.returncode == 0, r.stdout + r.stderr
    assert git(remote, "rev-parse", "refs/heads/release/demo") == v2


def test_other_slug_with_same_prefix_is_ignored(tmp_path):
    work, remote = make_repo(tmp_path)
    git(work, "push", "-q", "origin", "HEAD:refs/heads/release/demo-veg-v7")
    r = release(work, "pocs/demo", "demo")
    assert r.returncode == 0, r.stderr
    assert git(remote, "rev-parse", "refs/heads/release/demo-v1")


def test_script_never_force_pushes_or_tags():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "--force" not in text and "push -f" not in text and "+refs" not in text
    assert "refs/tags" not in text and "git tag" not in text
