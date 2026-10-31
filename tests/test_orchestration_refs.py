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
# Only a maintainer updates this hash, after reading the change themselves (see CONTRIBUTING.md).
HARD_LIMITS_SHA256 = "875b87d7939c4e4af233ad2bb68f24eaf8842c6d9409bcb3a1ea56688c8d3479"


def test_hard_limits_unchanged():
    import hashlib
    digest = hashlib.sha256((ORCH / "HARD_LIMITS.md").read_bytes()).hexdigest()
    assert digest == HARD_LIMITS_SHA256, (
        "orchestration/HARD_LIMITS.md changed. Process PRs may not touch it; "
        "if a maintainer changed it on purpose, they update HARD_LIMITS_SHA256 (see CONTRIBUTING.md)."
    )


def test_retro_loop_is_fenced():
    retro = (ORCH / "RETRO_BRIEF.md").read_text(encoding="utf-8")
    assert "HARD_LIMITS.md" in retro and "off-limits" in retro
    assert "make verify" in retro
    rnd = (ORCH / "RND.md").read_text(encoding="utf-8")
    assert "FAIL it if it touches `HARD_LIMITS.md`" in rnd


def test_release_cut_is_gated():
    rnd = (ORCH / "RND.md").read_text(encoding="utf-8")
    assert "$TOOLKIT/plugins/ticket-loop/scripts/release.sh" in rnd
    assert "release check" in rnd and "RELEASE: BLOCKED" in rnd
    launch = (ORCH / "LAUNCH_BRIEF.md").read_text(encoding="utf-8")
    assert "release/<slug>" in launch and "never `main`" in launch


def test_new_poc_every_night_without_caps():
    rnd = (ORCH / "RND.md").read_text(encoding="utf-8")
    nightly = (ORCH / "NIGHTLY.md").read_text(encoding="utf-8")
    assert "Part A" in rnd and "Part B" in rnd
    assert "Tonight's new POC comes first" in nightly
    assert "fewer than **2** issues" not in rnd  # no launch-queue cap
    assert "never start a second POC" not in rnd


def test_releases_are_branches_not_tags():
    for name in ("RND.md", "PRODUCT_EVAL_BRIEF.md", "LAUNCH_BRIEF.md", "HARD_LIMITS.md"):
        text = (ORCH / name).read_text(encoding="utf-8")
        assert "`<slug>-vN` tag" not in text and "release tag" not in text, name
    assert "release/<slug>-vN" in (ORCH / "RND.md").read_text(encoding="utf-8")


def test_settings_placeholders_are_documented_and_no_personal_values():
    import re
    settings = (ORCH / "SETTINGS.md").read_text()
    documented = set(re.findall(r"^\| `([A-Z_]+)` \|", settings, re.M)) | {"POC_DIR", "TOOLKIT_DIR"}
    for path in ORCH.glob("*.md"):
        if path.name == "SETTINGS.md":
            continue
        text = path.read_text()
        for key in re.findall(r"\{\{([A-Z_]+)\}\}", text):
            assert key in documented, f"{path.name} uses undocumented setting {key}"
    for name in ["NIGHTLY.md", "RND.md", "GROWTH_BRIEF.md", "LAUNCH_BRIEF.md",
                 "RESEARCH_BRIEF.md", "RETRO_BRIEF.md", "PRODUCT_EVAL_BRIEF.md"]:
        text = (ORCH / name).read_text()
        for personal in ["ImHereForTheCookies", "trig_0", "~/work", "Robert"]:
            assert personal not in text, f"{name} still hard-codes {personal}"
