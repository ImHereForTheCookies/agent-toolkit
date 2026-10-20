"""The nightly runbook and briefs only point at toolkit files that exist."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORCH = ROOT / "orchestration"
REF_RE = re.compile(r"\$TOOLKIT/([A-Za-z0-9_./-]+)")


def _docs():
    return sorted(ORCH.glob("*.md"))


def test_toolkit_paths_in_runbooks_exist():
    missing = []
    for doc in _docs():
        for ref in REF_RE.findall(doc.read_text(encoding="utf-8")):
            ref = ref.rstrip(".,)`")
            if not (ROOT / ref).exists():
                missing.append(f"{doc.name}: $TOOLKIT/{ref}")
    assert not missing, "dangling references:\n" + "\n".join(missing)


def test_rnd_units_have_their_briefs():
    rnd = (ORCH / "RND.md").read_text(encoding="utf-8")
    for brief in (
        "RESEARCH_BRIEF.md", "GROWTH_BRIEF.md", "LAUNCH_BRIEF.md",
        "PRODUCT_EVAL_BRIEF.md", "RETRO_BRIEF.md", "HARD_LIMITS.md",
    ):
        assert brief in rnd, f"RND.md should dispatch {brief}"
        assert (ORCH / brief).exists()


def test_nightly_hands_off_to_rnd_and_keeps_hard_limits():
    nightly = (ORCH / "NIGHTLY.md").read_text(encoding="utf-8")
    assert "$TOOLKIT/orchestration/RND.md" in nightly
    assert "$TOOLKIT/orchestration/HARD_LIMITS.md" in nightly
    for phrase in ("Never deploy", "never create accounts", "spend money", "Morning cutoff"):
        assert phrase in nightly, f"NIGHTLY.md lost: {phrase}"


def test_research_briefs_never_post():
    for name in ("RESEARCH_BRIEF.md", "GROWTH_BRIEF.md", "LAUNCH_BRIEF.md", "RETRO_BRIEF.md"):
        text = (ORCH / name).read_text(encoding="utf-8").lower()
        assert "never" in text and "post" in text, f"{name} must forbid posting"


# Pinned so the self-improving retro loop cannot rewrite the hard limits.
# Only Robert updates this hash, after reading the change himself.
HARD_LIMITS_SHA256 = "e7c644c5dd2e4ee1a2b0f0859a8b9f922ab87331706d72e463ffc1252d0e322e"


def test_hard_limits_unchanged():
    import hashlib
    digest = hashlib.sha256((ORCH / "HARD_LIMITS.md").read_bytes()).hexdigest()
    assert digest == HARD_LIMITS_SHA256, (
        "orchestration/HARD_LIMITS.md changed. Process PRs may not touch it; "
        "if Robert changed it on purpose, he updates HARD_LIMITS_SHA256."
    )


def test_retro_loop_is_fenced():
    retro = (ORCH / "RETRO_BRIEF.md").read_text(encoding="utf-8")
    assert "HARD_LIMITS.md" in retro and "off-limits" in retro
    assert "make verify" in retro
    rnd = (ORCH / "RND.md").read_text(encoding="utf-8")
    assert "FAIL it if it touches `HARD_LIMITS.md`" in rnd
