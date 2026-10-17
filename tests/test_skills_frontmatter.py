"""Every plugin skill has valid, trigger-focused frontmatter and a lean body.

`claude plugin validate` does not check SKILL.md frontmatter, so verify it here.
"""
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SKILLS = sorted(ROOT.glob("plugins/*/skills/*/SKILL.md"))


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert m, "missing --- frontmatter block"
    fields = {}
    for line in m.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def test_skills_exist():
    names = {p.parent.name for p in SKILLS}
    assert {"ticket-spec", "decompose-project"} <= names


@pytest.mark.parametrize("path", SKILLS, ids=lambda p: p.parent.name)
def test_skill_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    fm = frontmatter(text)
    assert fm.get("name") == path.parent.name
    assert not re.search(r"claude|anthropic", fm["name"], re.IGNORECASE)
    assert fm.get("description"), "description is required"
    assert fm["description"].startswith("Use when"), "describe WHEN to use the skill"
    assert len(text.splitlines()) <= 150, "keep SKILL.md under ~150 lines"
