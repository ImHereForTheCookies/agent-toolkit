"""The ticket-loop plugin stays routable, portable and plugin-first."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "ticket-loop"
SKILLS = PLUGIN / "skills"
REF_RE = re.compile(r"\$TOOLKIT/([A-Za-z0-9_./-]+)")


def _routes():
    rows = {}
    for line in (PLUGIN / "ROUTES.md").read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and cells[0] not in ("Label", "---") and not cells[0].startswith("-"):
            rows[cells[0]] = cells[1]
    return rows


def test_core_routes_exist():
    assert {"design", "plan", "build", "research", "evaluate"} <= set(_routes())


def test_every_route_points_at_a_skill():
    for label, skill in _routes().items():
        assert (SKILLS / skill / "SKILL.md").exists(), f"route {label} -> missing skill {skill}"


def test_every_skill_prefers_existing_plugins_first():
    for path in SKILLS.glob("*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        assert "## Prefer existing plugins" in text, f"{path.parent.name} lacks a plugin-first section"


def test_toolkit_paths_exist():
    missing = []
    for path in PLUGIN.rglob("*.md"):
        for ref in REF_RE.findall(path.read_text(encoding="utf-8")):
            ref = ref.rstrip(".,)`")
            if not (ROOT / ref).exists():
                missing.append(f"{path.relative_to(ROOT)}: $TOOLKIT/{ref}")
    assert not missing, "dangling references:\n" + "\n".join(missing)


def test_scheduled_prompt_is_short_and_personal_free():
    text = (PLUGIN / "templates" / "scheduled-prompt.md").read_text(encoding="utf-8")
    assert len(text.splitlines()) <= 20, "the private prompt must stay small"
    assert "run-queue/SKILL.md" in text
    for personal in ("ROB", "Robert", "cajunt", "notion.so"):
        assert personal not in text, f"template names {personal!r}"


def test_shared_skills_name_no_personal_ids():
    for path in SKILLS.glob("*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        for personal in ("ROB-", "team ROB", "Robert", "cajunt", "trig_"):
            assert personal not in text, f"{path.parent.name} names {personal!r}"


def test_hard_limits_keep_their_teeth():
    text = (PLUGIN / "HARD_LIMITS.md").read_text(encoding="utf-8")
    for phrase in ("Never deploy", "spend money", "Never force-push", "secrets", "Never block waiting"):
        assert phrase in text


def test_run_queue_wires_hard_limits_routes_and_chaining():
    text = (SKILLS / "run-queue" / "SKILL.md").read_text(encoding="utf-8")
    assert "$TOOLKIT/plugins/ticket-loop/HARD_LIMITS.md" in text
    assert "$TOOLKIT/plugins/ticket-loop/ROUTES.md" in text
    assert "fire_trigger" in text and "One unit only" in text
    assert "Concurrency guard" in text


def test_design_is_autonomous():
    text = (SKILLS / "design-system" / "SKILL.md").read_text(encoding="utf-8")
    assert "Assumptions" in text and "never ask" in text
    assert "templates/design-doc.md" in text


def test_pending_merges_and_red_main_cannot_stall_the_queue():
    rq = (SKILLS / "run-queue" / "SKILL.md").read_text(encoding="utf-8")
    bt = (SKILLS / "build-ticket" / "SKILL.md").read_text(encoding="utf-8")
    assert "Awaiting Merge" in rq and "Awaiting Merge" in bt
    assert "**without** `Awaiting Merge`" in rq
    assert "Fix red main" in rq and "Do not label it Needs Human" in bt
    assert "--allow-empty" in bt  # empty repos get a main to open PRs against
    assert "Chain started:" in rq
    assert "any ticket with an assignee" in rq  # humans working by hand are never collided with


def test_evaluation_rounds_are_capped_and_releases_opt_in():
    rq = (SKILLS / "run-queue" / "SKILL.md").read_text(encoding="utf-8")
    ev = (SKILLS / "evaluate-project" / "SKILL.md").read_text(encoding="utf-8")
    assert "fewer than 3 evaluate tickets" in rq
    assert "Releases: <slug>" in ev and "never create release branches" in ev


def test_research_findings_flow_into_requirements():
    rq = (SKILLS / "run-queue" / "SKILL.md").read_text(encoding="utf-8")
    ds = (SKILLS / "design-system" / "SKILL.md").read_text(encoding="utf-8")
    rs = (SKILLS / "research-question" / "SKILL.md").read_text(encoding="utf-8")
    tpl = (PLUGIN / "templates" / "design-doc.md").read_text(encoding="utf-8")
    assert "Incorporate research findings" in rq
    assert "Incorporated" in ds and "Rejected" in ds and "research` tickets" in ds
    assert "Needs human research" in rs and "never post" in rs
    assert "## Research and evidence" in tpl and "R1." in tpl


def test_plans_are_modular_so_merges_never_block():
    pl = (SKILLS / "plan-tickets" / "SKILL.md").read_text(encoding="utf-8")
    rq = (SKILLS / "run-queue" / "SKILL.md").read_text(encoding="utf-8")
    assert "Modular by default" in pl and "registry" in pl
    assert "Prefer independent work" in rq
