#!/usr/bin/env python3
"""Check the machine-checkable lines of REQUIREMENTS.md (CLIs and Python modules).

Connector (`mcp:`) and plugin (`plugin:`) lines can only be checked by the agent
from inside its session; they are listed so the agent knows what to verify.
Usage: check_requirements.py [path/to/REQUIREMENTS.md]
Exit 0 when every required cli line is met, 1 otherwise.
"""
import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # the toolkit checkout holding REQUIREMENTS.md


def manifest(text):
    block = re.search(r"## Manifest\s+```\n(.*?)```", text, re.S)
    assert block, "REQUIREMENTS.md has no Manifest block"
    rows = []
    for line in block.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        head, *rest = [p.strip() for p in line.split("|")]
        optional = head.startswith("optional ")
        kind, _, name = head.removeprefix("optional ").partition(":")
        rows.append({"kind": kind.strip(), "name": name.strip(), "optional": optional,
                     "needed_by": rest[0] if rest else "", "check": rest[1] if len(rest) > 1 else ""})
    return rows


def check_cli(name):
    m = re.match(r"([\w.-]+)(>=([\d.]+))?$", name)
    binary, minimum = m.group(1), m.group(3)
    if binary == "python3":
        have = ".".join(map(str, sys.version_info[:3]))
        ok = not minimum or tuple(map(int, have.split("."))) >= tuple(map(int, minimum.split(".")))
        return ok, f"python {have}" + (f" (need >= {minimum})" if not ok else "")
    path = shutil.which(binary)
    if not path:
        return False, "not found on PATH"
    if binary == "gh":
        authed = subprocess.run(["gh", "auth", "status"], capture_output=True).returncode == 0
        return True, path + ("" if authed else " (not authenticated: run gh auth login)")
    return True, path


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "REQUIREMENTS.md"
    rows = manifest(path.read_text(encoding="utf-8"))
    failed = 0
    for r in rows:
        tag = "optional " if r["optional"] else ""
        if r["kind"] == "cli":
            ok, detail = check_cli(r["name"])
        elif r["kind"] == "python":
            ok, detail = importlib.util.find_spec(r["name"]) is not None, r["name"]
        else:
            print(f"?    {tag}{r['kind']}: {r['name']}  (agent checks in-session: {r['check']})")
            continue
        status = "ok  " if ok else ("warn" if r["optional"] else "FAIL")
        print(f"{status} {tag}{r['kind']}: {r['name']}  {detail}")
        failed += (not ok) and not r["optional"]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
