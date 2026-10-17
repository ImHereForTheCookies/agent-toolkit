"""harness_init.py turns an empty dir into a project any worker can start cold in."""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "plugins/project-template/scripts/harness_init.py"
FILES = ["CLAUDE.md", "PROGRESS.md", "Makefile", ".claude/settings.json"]
PLUGINS = ["agentic-workflow", "code-navigation", "linear-workflow", "project-template"]


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                          capture_output=True, text=True)


def test_creates_files(tmp_path):
    target = tmp_path / "myproj"
    r = run(target)
    assert r.returncode == 0, r.stderr
    for f in FILES:
        assert (target / f).is_file(), f
        assert f"created: {f}" in r.stdout
    assert (target / ".git").exists(), "git init should run in a non-repo"
    assert "{{" not in (target / "CLAUDE.md").read_text()
    assert "myproj" in (target / "CLAUDE.md").read_text()


def test_name_option(tmp_path):
    run(tmp_path, "--name", "Pantry")
    assert (tmp_path / "CLAUDE.md").read_text().startswith("# Pantry")
    assert "Pantry" in (tmp_path / "PROGRESS.md").read_text()


def test_settings(tmp_path):
    run(tmp_path)
    s = json.loads((tmp_path / ".claude/settings.json").read_text())
    assert s["extraKnownMarketplaces"] == {
        "agent-toolkit": {"source": {"source": "github", "repo": "ImHereForTheCookies/agent-toolkit"}}
    }
    assert s["enabledPlugins"] == {f"{p}@agent-toolkit": True for p in PLUGINS}


def test_idempotent(tmp_path):
    run(tmp_path)
    for f in FILES:
        (tmp_path / f).write_text("MINE\n")
    r = run(tmp_path)
    assert r.returncode == 0
    for f in FILES:
        assert (tmp_path / f).read_text() == "MINE\n", f"{f} was overwritten"
        assert f"skipped (exists): {f}" in r.stdout
    r = run(tmp_path, "--force")
    assert (tmp_path / "CLAUDE.md").read_text() != "MINE\n"
    assert "overwritten: CLAUDE.md" in r.stdout


def test_existing_repo_left_alone(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    head = (tmp_path / ".git/HEAD").read_text()
    r = run(tmp_path)
    assert "already a repo" in r.stdout
    assert (tmp_path / ".git/HEAD").read_text() == head


def test_claude_md_short(tmp_path):
    template = ROOT / "plugins/project-template/templates/CLAUDE.md"
    assert len(template.read_text().splitlines()) < 60
    run(tmp_path, "--name", "x")
    assert len((tmp_path / "CLAUDE.md").read_text().splitlines()) < 60
    text = (tmp_path / "CLAUDE.md").read_text()
    for heading in ("Stack", "Commands", "Architecture decisions", "Gotchas", "Workflow"):
        assert re.search(rf"^## {heading}$", text, re.M), heading


def test_makefile_contract(tmp_path):
    run(tmp_path)
    for target in ("dev", "test", "e2e", "verify", "symbols"):
        r = subprocess.run(["make", "-s", "-C", str(tmp_path), target], capture_output=True, text=True)
        assert r.returncode == 0, (target, r.stderr)
    out = subprocess.run(["make", "-s", "-C", str(tmp_path), "test"], capture_output=True, text=True).stdout
    assert "TODO: define test for this project" in out
