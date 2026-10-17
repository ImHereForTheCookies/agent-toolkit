"""Structure checks for evals/hitl/scenarios.json (the eval itself costs API calls and is not run here)."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCEN = json.loads((ROOT / "evals/hitl/scenarios.json").read_text(encoding="utf-8"))
SKILL = ROOT / "plugins/agentic-workflow/skills/human-in-the-loop/SKILL.md"
ACTIONS = {
    "escalate_needs_human", "stop_before_action", "file_followup_ticket_and_continue",
    "merge_and_flag_taste", "pr_without_merge", "proceed",
}


def load_runner():
    spec = importlib.util.spec_from_file_location("run_eval", ROOT / "evals/hitl/run_eval.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_six_scenarios_with_required_fields():
    assert len(SCEN) == 6
    for sc in SCEN:
        assert set(sc) == {"id", "situation", "expected_action"}
        assert sc["id"] and sc["situation"].strip()
        assert sc["expected_action"] in ACTIONS


def test_ids_unique():
    ids = [s["id"] for s in SCEN]
    assert len(set(ids)) == len(ids)


def test_covers_a_proceed_case_and_the_demo3_case():
    actions = [s["expected_action"] for s in SCEN]
    assert "proceed" in actions
    assert any("DEMO-3" in s["situation"] and s["expected_action"] == "escalate_needs_human" for s in SCEN)


def test_situation_does_not_leak_the_label():
    for sc in SCEN:
        assert sc["expected_action"] not in sc["situation"]


def test_runner_actions_match_skill_and_parser():
    run = load_runner()
    assert set(run.ACTIONS) == ACTIONS
    text = SKILL.read_text(encoding="utf-8")
    for a in ACTIONS:
        assert f"`{a}`" in text, f"skill does not name action {a}"
    assert run.parse_label("proceed\n") == "proceed"
    assert run.parse_label("Action: `pr_without_merge`.") == "pr_without_merge"
    assert run.parse_label("proceed or escalate_needs_human") is None
