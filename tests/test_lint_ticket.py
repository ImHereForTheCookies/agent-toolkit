import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "lint_ticket.py"

_spec = importlib.util.spec_from_file_location("lint_ticket", SCRIPT)
lint_ticket = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lint_ticket)

SECTIONS = ["Goal", "Context", "Acceptance criteria", "Verify", "Out of scope", "Escalation"]

VALID = """\
# ROB-X: Example

## Goal
Do the thing.

## Context
- some context

## Acceptance criteria
- [ ] It works - checked by: tests/test_x.py::test_works
- [x] It is fast - checked by: make verify
- plain bullet item - checked by: manual review

## Verify
make verify

## Out of scope
Everything else.

## Escalation
none
"""


def run_cli(*args, stdin=None):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


def drop_section(text, name):
    """Remove a `## name` heading and its body from VALID-style text."""
    out, skipping = [], False
    for line in text.splitlines(keepends=True):
        if line.startswith("## "):
            skipping = line[3:].strip().lower() == name.lower()
        if not skipping:
            out.append(line)
    return "".join(out)


def test_valid(tmp_path):
    assert lint_ticket.lint(VALID) == []
    f = tmp_path / "t.md"
    f.write_text(VALID)
    r = run_cli(str(f))
    assert r.returncode == 0
    assert r.stdout == ""


def test_valid_case_insensitive_headings_and_backticked_escalation():
    text = VALID.replace("## Acceptance criteria", "## ACCEPTANCE Criteria")
    text = text.replace("\nnone\n", "\n`Taste-Checkpoint`\n")
    assert lint_ticket.lint(text) == []


def test_missing_sections(tmp_path):
    for name in SECTIONS:
        text = drop_section(VALID, name)
        problems = lint_ticket.lint(text)
        assert problems, name
        assert any(name in p for p in problems), (name, problems)

        f = tmp_path / f"{name.replace(' ', '_')}.md"
        f.write_text(text)
        r = run_cli(str(f))
        assert r.returncode == 1
        assert name in r.stdout
        assert r.stdout.startswith(f"{f}: ")


def test_unchecked_criterion(tmp_path):
    text = VALID.replace(
        "- [ ] It works - checked by: tests/test_x.py::test_works",
        "- [ ] It works but nobody checks it",
    )
    problems = lint_ticket.lint(text)
    assert len(problems) == 1
    assert "It works but nobody checks it" in problems[0]

    # `checked by:` with nothing after it is also a failure
    empty = VALID.replace("checked by: make verify", "checked by:   ")
    assert any("It is fast" in p for p in lint_ticket.lint(empty))

    f = tmp_path / "t.md"
    f.write_text(text)
    r = run_cli(str(f))
    assert r.returncode == 1
    assert "checked by" in r.stdout


def test_no_criteria_items():
    text = VALID.replace("- [ ] It works - checked by: tests/test_x.py::test_works\n", "")
    text = text.replace("- [x] It is fast - checked by: make verify\n", "")
    text = text.replace("- plain bullet item - checked by: manual review\n", "")
    problems = lint_ticket.lint(text)
    assert any("no criteria" in p for p in problems)


def test_bad_escalation(tmp_path):
    text = VALID.replace("\nnone\n", "\nmaybe\n")
    problems = lint_ticket.lint(text)
    assert len(problems) == 1
    assert "maybe" in problems[0]

    f = tmp_path / "t.md"
    f.write_text(text)
    r = run_cli(str(f))
    assert r.returncode == 1
    assert "Escalation" in r.stdout


def test_empty_escalation_section():
    text = VALID.replace("## Escalation\nnone\n", "## Escalation\n\n")
    assert any("Escalation" in p for p in lint_ticket.lint(text))


def test_cli_stdin_and_multiple_files(tmp_path):
    assert run_cli("-", stdin=VALID).returncode == 0
    r = run_cli("-", stdin="# nothing\n")
    assert r.returncode == 1
    assert r.stdout.startswith("-: missing section: Goal")

    good = tmp_path / "good.md"
    good.write_text(VALID)
    bad = tmp_path / "bad.md"
    bad.write_text(drop_section(VALID, "Verify"))
    r = run_cli(str(good), str(bad))
    assert r.returncode == 1
    lines = r.stdout.splitlines()
    assert lines and all(ln.startswith(f"{bad}: ") for ln in lines)


def test_cli_unreadable_file(tmp_path):
    r = run_cli(str(tmp_path / "nope.md"))
    assert r.returncode == 1
    assert "nope.md" in r.stdout


def test_star_bullets_accepted():
    """Linear renders bullets as '*'; the linter must accept '*' and '+' markers."""
    text = (
        "## Goal\nx\n## Context\nx\n## Acceptance criteria\n"
        "* [ ] a thing — checked by: make verify\n"
        "+ another — checked by: tests/test_x.py\n"
        "## Verify\nmake verify\n## Out of scope\nx\n## Escalation\nnone\n"
    )
    assert lint_ticket.lint(text) == []
