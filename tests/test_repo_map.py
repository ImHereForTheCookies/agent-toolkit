"""repo_map.py writes a compact, deterministic symbol index."""
import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "plugins/code-navigation/scripts/repo_map.py"
FIXTURE = ROOT / "fixtures/demo-project"


def run(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                          capture_output=True, text=True)


def file_lines(stdout):
    return [l for l in stdout.splitlines() if not l.startswith(("#", "..."))]


def test_fixture_complete():
    r = run(FIXTURE)
    assert r.returncode == 0, r.stderr
    by_path = {l.split(":", 1)[0]: l for l in file_lines(r.stdout)}
    modules = {p.relative_to(FIXTURE).as_posix() for p in FIXTURE.rglob("*.py")
               if ".venv" not in p.parts and "__pycache__" not in p.parts}
    assert modules == set(by_path)
    for mod in modules:
        tree = ast.parse((FIXTURE / mod).read_text())
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                assert f"{node.name}(L{node.lineno})" in by_path[mod], (mod, node.name)
                if isinstance(node, ast.ClassDef):
                    for sub in node.body:
                        if isinstance(sub, ast.FunctionDef):
                            assert f"{node.name}.{sub.name}(L{sub.lineno})" in by_path[mod]
    assert list(by_path) == sorted(by_path)


def test_header_and_deterministic(tmp_path):
    a, b = tmp_path / "a/symbols.md", tmp_path / "b.md"
    assert run(FIXTURE, "--out", a).returncode == 0
    assert run(FIXTURE, "--out", b).returncode == 0
    assert a.read_bytes() == b.read_bytes()
    first = a.read_text().splitlines()[0]
    assert first.startswith("#") and "repo_map.py" in first and "do not edit" in first


def test_size_cap():
    full = run(FIXTURE).stdout
    cap = len(full.encode()) // 2
    r = run(FIXTURE, "--max-bytes", cap)
    assert r.returncode == 0
    assert len(r.stdout.encode()) <= cap
    last = r.stdout.splitlines()[-1]
    assert last.startswith("... truncated (") and last.endswith(" more files)")
    n = int(last.split("(")[1].split()[0])
    assert n == len(file_lines(full)) - len(file_lines(r.stdout))
    for line in r.stdout.splitlines()[:-1]:
        assert line in full.splitlines(), "partial line emitted"
    assert "truncated" not in run(FIXTURE, "--max-bytes", len(full.encode())).stdout


def test_skips_vendored(tmp_path):
    for d in (".venv", "venv", "node_modules", "__pycache__", "dist", "build", ".hidden", "pkg/.cache"):
        (tmp_path / d).mkdir(parents=True)
        (tmp_path / d / "x.py").write_text("def hidden(): pass\n")
        (tmp_path / d / "x.js").write_text("function hidden() {}\n")
    (tmp_path / "keep.py").write_text("def kept(): pass\n")
    out = run(tmp_path).stdout
    assert "kept(L1)" in out
    assert "hidden" not in out
    assert len(file_lines(out)) == 1


def test_js_ts_and_python_methods(tmp_path):
    (tmp_path / "a.js").write_text(
        "function plain() {}\n"
        "  function nested() {}\n"
        "export default async function main() {}\n"
        "export function named() {}\n"
        "class Widget {}\n"
        "export class Exported {}\n"
        "const arrow = (a, b) => a + b;\n"
        "export const asyncArrow = async (x) => x;\n"
        "const single = x => x;\n"
        "const notFn = 3;\n")
    (tmp_path / "b.ts").write_text("export const typed = (a: number): number => a;\n")
    (tmp_path / "c.py").write_text(
        "class A:\n    def m(self): pass\n    class Inner:\n        def deep(self): pass\n\n"
        "async def go(): pass\n")
    lines = {l.split(":", 1)[0]: l.split(": ", 1)[1] for l in file_lines(run(tmp_path).stdout)}
    assert lines["a.js"] == ("plain(L1), main(L3), named(L4), Widget(L5), Exported(L6), "
                             "arrow(L7), asyncArrow(L8), single(L9)")
    assert lines["b.ts"] == "typed(L1)"
    assert lines["c.py"] == "A(L1), A.m(L2), go(L6)"


def test_syntax_error_and_bad_root(tmp_path):
    (tmp_path / "bad.py").write_text("def (:\n")
    assert "bad.py:" in run(tmp_path).stdout
    r = run(tmp_path / "missing")
    assert r.returncode == 2
