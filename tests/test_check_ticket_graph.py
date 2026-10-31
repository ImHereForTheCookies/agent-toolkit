import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "plugins" / "agentic-workflow" / "scripts" / "check_ticket_graph.py"

_spec = importlib.util.spec_from_file_location("check_ticket_graph", SCRIPT)
graph = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(graph)


def write(tmp_path, tickets):
    """tickets: {id: [blockers]} -> ticket files in tmp_path."""
    for tid, blockers in tickets.items():
        lines = ["Status: Backlog", "", f"# {tid} Do {tid}", ""]
        if blockers:
            lines += [f"Blocked by: {', '.join(blockers)}", ""]
        lines += ["## Goal", "x", ""]
        (tmp_path / f"{tid}.md").write_text("\n".join(lines), encoding="utf-8")


def run(path):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True
    )


def test_valid_dag_passes_and_prints_topological_order(tmp_path):
    write(tmp_path, {"T-1": [], "T-2": ["T-1"], "T-3": ["T-1"], "T-4": ["T-2", "T-3"]})
    result = run(tmp_path)
    assert result.returncode == 0, result.stdout
    order = result.stdout.split("order: ")[1].strip().split(" -> ")
    assert sorted(order) == ["T-1", "T-2", "T-3", "T-4"]
    for tid, blockers in {"T-2": ["T-1"], "T-3": ["T-1"], "T-4": ["T-2", "T-3"]}.items():
        assert all(order.index(b) < order.index(tid) for b in blockers)


def test_cycle_fails(tmp_path):
    write(tmp_path, {"T-1": ["T-3"], "T-2": ["T-1"], "T-3": ["T-2"]})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "cycle" in result.stdout


def test_reference_to_missing_ticket_fails(tmp_path):
    write(tmp_path, {"T-1": [], "T-2": ["T-9"]})
    result = run(tmp_path)
    assert result.returncode == 1
    assert "T-2: blocked by unknown ticket T-9" in result.stdout


def test_self_reference_and_duplicate_id_fail(tmp_path):
    assert graph.check_graph({"T-1": ["T-1"]})[1]
    write(tmp_path, {"T-1": []})
    (tmp_path / "copy.md").write_text("# T-1 Duplicate\n", encoding="utf-8")
    assert run(tmp_path).returncode == 1


def test_blocked_by_inside_code_fence_is_ignored(tmp_path):
    (tmp_path / "T-1.md").write_text(
        "# T-1 Example\n\n```\nBlocked by: NOPE-1\n```\n", encoding="utf-8"
    )
    assert run(tmp_path).returncode == 0


def test_empty_directory_fails(tmp_path):
    assert run(tmp_path).returncode == 1
