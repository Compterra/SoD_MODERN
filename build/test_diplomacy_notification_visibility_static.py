from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_guarded_before(raw: str, message: str, guard: str, window: int = 360) -> None:
    idx = raw.find(message)
    assert idx >= 0, f"missing message: {message}"
    before = raw[max(0, idx - window):idx]
    assert guard in before, f"{message!r} is not guarded by {guard!r}"


def test_imperial_diplomatic_dispatch_broadcasts_are_debug_only() -> None:
    war = read("src/scripts/ZF_factions/diplomacy_start_war_between_kingdoms.py")
    peace = read("src/scripts/ZF_factions/diplomacy_start_peace_between_kingdoms.py")
    assert_guarded_before(war, "Diplomatic dispatch: {s1} and {s2} are at war", '(eq, "$g_sod_debug", 1)')
    assert_guarded_before(peace, "Diplomatic dispatch: {s1} and {s2} have paused hostilities", '(eq, "$g_sod_debug", 1)')


def test_random_diplomatic_incident_notifications_are_player_relevant_or_debug() -> None:
    raw = read("src/scripts/ZY_helper_scripts/sod_diplomacy_system.py")
    assert_guarded_before(raw, "Diplomatic incident: {s39} has soured relations", '(le, "$g_sod_diplomacy_notification_level", 0)', 460)
    assert_guarded_before(raw, "Diplomatic incident: {s39} has soured relations", '(this_or_next|eq, "$g_sod_debug", 1)', 460)
    assert_guarded_before(raw, "Diplomatic incident: {s39} has soured relations", '(this_or_next|eq, ":source_faction", fac_player_supporters_faction)', 460)
    assert_guarded_before(raw, "Diplomatic incident: {s39} has soured relations", '(eq, ":target_faction", fac_player_supporters_faction)', 460)
