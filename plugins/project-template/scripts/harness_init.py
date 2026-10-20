#!/usr/bin/env python3
"""Turn a directory into a project any worker can start cold in.

Copies the templates (CLAUDE.md, PROGRESS.md, Makefile, .claude/settings.json)
into <dir>, substituting {{PROJECT_NAME}}, and runs `git init` if <dir> is not
already a git repo or inside one (a folder in a monorepo, e.g. cajunt/pocs/<slug>). Existing files are never overwritten unless --force.

Usage: harness_init.py <dir> [--name NAME] [--force]
"""
import argparse
import subprocess
import sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
PLACEHOLDER = "{{PROJECT_NAME}}"


def template_files():
    """Relative paths of every file under templates/, sorted."""
    return sorted(p.relative_to(TEMPLATES) for p in TEMPLATES.rglob("*") if p.is_file())


def _inside_work_tree(path):
    """True when path sits inside an existing git work tree (e.g. a monorepo subfolder)."""
    probe = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True,
    )
    return probe.returncode == 0 and probe.stdout.strip() == "true"


def init(target, name=None, force=False):
    """Create the harness files in target. Returns (created, overwritten, skipped, git_inited)."""
    target = Path(target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    name = name or target.name
    created, overwritten, skipped = [], [], []
    for rel in template_files():
        dest = target / rel
        existed = dest.exists()
        if existed and not force:
            skipped.append(str(rel))
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        text = (TEMPLATES / rel).read_text(encoding="utf-8").replace(PLACEHOLDER, name)
        dest.write_text(text, encoding="utf-8")
        (overwritten if existed else created).append(str(rel))
    git_inited = False
    if not (target / ".git").exists() and not _inside_work_tree(target):
        subprocess.run(["git", "init", "-q", str(target)], check=True)
        git_inited = True
    return created, overwritten, skipped, git_inited


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dir", help="project directory (created if missing)")
    ap.add_argument("--name", help="project name (default: the directory name)")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    args = ap.parse_args(argv)
    try:
        created, overwritten, skipped, git_inited = init(args.dir, args.name, args.force)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"harness_init: {exc}", file=sys.stderr)
        return 1
    for label, files in (("created", created), ("overwritten", overwritten), ("skipped (exists)", skipped)):
        for f in files:
            print(f"{label}: {f}")
    print("git: initialized new repo" if git_inited else "git: already a repo (or inside one), left alone")
    return 0


if __name__ == "__main__":
    sys.exit(main())
