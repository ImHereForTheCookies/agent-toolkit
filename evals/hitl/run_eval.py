#!/usr/bin/env python3
"""Run the human-in-the-loop eval: does a fresh agent given only the skill pick the right action?

For each scenario in scenarios.json this calls `claude -p` once with the SKILL.md text and the
situation, asks for ONLY an action label, and compares it with expected_action. Costs API calls,
so it is NOT part of `make verify`; run it with `make eval-hitl`.

Usage: run_eval.py [--model MODEL] [--threshold N]
Exit 0 when score >= threshold (default 5 of the scenarios), 1 otherwise.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SKILL = ROOT / "plugins/agentic-workflow/skills/human-in-the-loop/SKILL.md"
ACTIONS = [
    "escalate_needs_human",
    "stop_before_action",
    "file_followup_ticket_and_continue",
    "merge_and_flag_taste",
    "pr_without_merge",
    "proceed",
]

SYSTEM = (
    "You are an unattended coding agent working a Linear ticket overnight. "
    "Follow the skill below exactly. Answer with ONLY one action label and nothing else."
)


def build_prompt(skill_text, situation):
    return (
        f"<skill>\n{skill_text}\n</skill>\n\n"
        f"<situation>\n{situation}\n</situation>\n\n"
        "Which single action do you take? Valid labels: " + ", ".join(ACTIONS) + ".\n"
        "Reply with ONLY the label, no punctuation or explanation."
    )


def parse_label(output):
    """Return the action label found in the model output, or None."""
    text = output.strip().lower()
    if text in ACTIONS:
        return text
    found = [a for a in ACTIONS if re.search(rf"\b{a}\b", text)]
    return found[0] if len(found) == 1 else None


def ask(prompt, model):
    cmd = ["claude", "-p", prompt, "--system-prompt", SYSTEM, "--tools", "",
           "--disable-slash-commands", "--setting-sources", "", "--strict-mcp-config",
           "--no-session-persistence"]
    if model:
        cmd += ["--model", model]
    with tempfile.TemporaryDirectory() as cwd:  # no CLAUDE.md or repo context leaks in
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=300)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"claude exited {proc.returncode}")
    return proc.stdout


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=None)
    ap.add_argument("--threshold", type=int, default=5)
    args = ap.parse_args(argv)

    scenarios = json.loads((HERE / "scenarios.json").read_text(encoding="utf-8"))
    skill_text = SKILL.read_text(encoding="utf-8")
    rows, score = [], 0
    for sc in scenarios:
        try:
            got = parse_label(ask(build_prompt(skill_text, sc["situation"]), args.model))
        except Exception as exc:  # a failed call counts as a miss, the run continues
            print(f"error on {sc['id']}: {exc}", file=sys.stderr)
            got = None
        ok = got == sc["expected_action"]
        score += ok
        rows.append((sc["id"], sc["expected_action"], got or "?", "PASS" if ok else "FAIL"))

    w = [max(len(r[i]) for r in rows + [("scenario", "expected", "got", "result")]) for i in range(4)]
    for r in [("scenario", "expected", "got", "result")] + rows:
        print("  ".join(c.ljust(w[i]) for i, c in enumerate(r)))
    print(f"\nscore: {score}/{len(scenarios)} (threshold {args.threshold})")
    return 0 if score >= args.threshold else 1


if __name__ == "__main__":
    sys.exit(main())
