"""linear-workflow plugin: .mcp.json shape and the linear-tickets skill contents."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "linear-workflow"
SKILL = PLUGIN / "skills" / "linear-tickets" / "SKILL.md"


def test_mcp_json_registers_linear_over_http():
    cfg = json.loads((PLUGIN / ".mcp.json").read_text(encoding="utf-8"))
    server = cfg["mcpServers"]["linear"]
    assert server["type"] == "http"
    assert server["url"] == "https://mcp.linear.app/mcp"
    assert server["headers"] == {"Authorization": "Bearer ${LINEAR_API_KEY}"}


def test_mcp_json_has_no_inline_secret():
    text = (PLUGIN / ".mcp.json").read_text(encoding="utf-8")
    assert "lin_api_" not in text


def test_skill_covers_the_workflow():
    text = SKILL.read_text(encoding="utf-8")
    for needle in (
        "Needs Human",
        "addLabels",
        "lint_ticket.py",
        "In Progress",
        "In Review",
        "**Evidence**",
        "LINEAR_API_KEY",
        "blockedBy",
    ):
        assert needle in text, f"SKILL.md should mention {needle!r}"
