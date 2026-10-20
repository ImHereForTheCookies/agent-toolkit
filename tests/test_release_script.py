"""orchestration/release.sh against a throwaway repo with a local bare remote."""
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "orchestration" / "release.sh"
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
    return subprocess.run(["bash", str(SCRIPT), str(work), folder, slug],
                          capture_output=True, text=True,
                          env={**os.environ, "RELEASE_SKIP_FETCH": "1",
                               "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                               "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})


def test_first_release_tags_and_moves_branch(tmp_path):
    work, remote = make_repo(tmp_path)
    r = release(work, "pocs/demo", "demo")
    assert r.returncode == 0, r.stderr
    head = git(work, "rev-parse", "HEAD")
    assert git(remote, "rev-parse", "refs/tags/demo-v1^{commit}") == head
    assert git(remote, "rev-parse", "refs/heads/release/demo") == head


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
    assert git(remote, "rev-parse", "refs/tags/demo-v2^{commit}") == head
    assert git(remote, "rev-parse", "refs/heads/release/demo") == head
    assert "feature two" in git(remote, "tag", "-l", "-n20", "demo-v2")


def test_failed_verify_cuts_nothing(tmp_path):
    work, remote = make_repo(tmp_path, verify_ok=False)
    r = release(work, "pocs/demo", "demo")
    assert r.returncode != 0
    assert git(remote, "tag", "-l") == ""


def test_root_project_ignores_pocs_changes(tmp_path):
    work, _ = make_repo(tmp_path)
    (work / "Makefile").write_text("verify:\n\t@true\n")
    git(work, "add", "-A")
    git(work, "commit", "-qm", "root makefile")
    assert release(work, ".", "rootapp").returncode == 0
    (work / "pocs/demo/app.js").write_text("poc only\n")
    git(work, "commit", "-qam", "poc change")
    assert release(work, ".", "rootapp").returncode == 3


def test_script_never_force_pushes():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "--force" not in text and "push -f" not in text and "+refs" not in text
