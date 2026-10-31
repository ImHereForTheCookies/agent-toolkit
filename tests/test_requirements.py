"""REQUIREMENTS.md is the contract for what the toolkit needs; keep it true."""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"

_spec = importlib.util.spec_from_file_location("check_requirements", ROOT / "plugins" / "ticket-loop" / "scripts" / "check_requirements.py")
check_requirements = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_requirements)

TEXT = (ROOT / "REQUIREMENTS.md").read_text(encoding="utf-8")
ROWS = check_requirements.manifest(TEXT)


def per_plugin_table():
    deps = {}
    for m in re.finditer(r"^\| ([a-z-]+) \| (.+?) \| (.+?) \|$", TEXT, re.M):
        name, needs, depends = m.groups()
        if name in {"Plugin", "---"} or name.startswith("-"):
            continue
        deps[name] = set(re.findall(r"[a-z]+-[a-z]+", depends)) & {p.name for p in PLUGINS.iterdir()}
    return deps


def plugin_files():
    for p in PLUGINS.rglob("*"):
        if p.is_file() and p.suffix in {".md", ".py", ".sh", ".json"} and "__pycache__" not in p.parts:
            yield p


def test_manifest_has_required_kinds():
    required = {(r["kind"], r["name"].split(">=")[0]) for r in ROWS if not r["optional"]}
    assert {("mcp", "Linear"), ("mcp", "Notion"), ("plugin", "superpowers"), ("cli", "git")} <= required


def test_every_plugin_is_in_the_table():
    assert set(per_plugin_table()) == {p.name for p in PLUGINS.iterdir() if p.is_dir()}


def test_connectors_used_are_listed():
    listed = {r["name"] for r in ROWS if r["kind"] == "mcp"}
    for f in list(plugin_files()) + list((ROOT / "orchestration").glob("*.md")):
        for server in re.findall(r"mcp__([A-Za-z][A-Za-z-]*)__", f.read_text(encoding="utf-8")):
            assert server in listed, f"{f.relative_to(ROOT)} uses mcp__{server}__ which REQUIREMENTS.md does not list"


def test_plugins_only_reach_into_declared_dependencies():
    deps = per_plugin_table()
    for f in plugin_files():
        own = f.relative_to(PLUGINS).parts[0]
        text = f.read_text(encoding="utf-8")
        for other in set(re.findall(r"plugins/([a-z]+-[a-z]+)/", text)) - {own}:
            if other in deps:
                assert other in deps[own], (
                    f"{f.relative_to(ROOT)} references plugin {other}, which {own} does not declare "
                    f"as a dependency in REQUIREMENTS.md")


def test_plugins_do_not_depend_on_the_authors_orchestration_folder():
    for f in plugin_files():
        text = f.read_text(encoding="utf-8")
        assert "$TOOLKIT/orchestration" not in text, f"{f.relative_to(ROOT)} depends on orchestration/"
        assert "$TOOLKIT/scripts" not in text, f"{f.relative_to(ROOT)} depends on repo-root scripts/"


def test_superpowers_is_required_not_optional_in_skills():
    for f in plugin_files():
        text = f.read_text(encoding="utf-8")
        assert not re.search(r"if (the )?superpowers[^.\n]{0,40}(is )?available", text, re.I), (
            f"{f.relative_to(ROOT)} treats superpowers as optional; it is required (REQUIREMENTS.md)")


def test_run_queue_does_preflight():
    text = (PLUGINS / "ticket-loop/skills/run-queue/SKILL.md").read_text(encoding="utf-8")
    assert "REQUIREMENTS.md" in text and "Preflight" in text
