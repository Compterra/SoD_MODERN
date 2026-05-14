from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_weekly_unusual_health_setback_only_reports_player_relevant_centers() -> None:
    raw = read("src/triggers/ST04_weekly/entry_0117.py")
    message_idx = raw.find("suffers an unusual health setback")
    assert message_idx >= 0
    before = raw[max(0, message_idx - 420):message_idx]
    assert '(eq, "$g_sod_hide_messages", 0)' in before
    assert '(store_faction_of_party, ":center_faction", ":center_no")' in before
    assert '(this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player")' in before
    assert '(eq, ":center_faction", "fac_player_supporters_faction")' in before


def test_weekly_unusual_health_setback_still_applies_simulation_after_report_gate() -> None:
    raw = read("src/triggers/ST04_weekly/entry_0117.py")
    message_idx = raw.find("suffers an unusual health setback")
    change_idx = raw.find('(assign, ":special_health_change", 1)', message_idx)
    assert change_idx > message_idx
    between = raw[message_idx:change_idx]
    assert "(try_end)," in between


def test_weekly_town_population_reports_only_player_controlled_centers() -> None:
    raw = read("src/triggers/ST04_weekly/entry_0101.py")
    message_idx = raw.find("Word reaches you from {s1}")
    assert message_idx >= 0
    before = raw[max(0, message_idx - 1400):message_idx]
    assert '(eq, "$g_sod_hide_messages", 0)' in before
    assert '(party_slot_eq, ":center_no", slot_town_lord, "trp_player")' in before
    assert '(eq, ":center_faction", "$players_kingdom")' in before
    assert 'severe enough' not in before
    assert '(ge, ":abs_growth", 20)' not in before
    assert '(lt, ":center_health", 35)' not in before


def test_weekly_village_population_reports_only_player_controlled_centers() -> None:
    raw = read("src/triggers/ST04_weekly/entry_0102.py")
    message_idx = raw.find("Word reaches you from {s1}")
    assert message_idx >= 0
    before = raw[max(0, message_idx - 1400):message_idx]
    assert '(eq, "$g_sod_hide_messages", 0)' in before
    assert '(party_slot_eq, ":center_no", slot_town_lord, "trp_player")' in before
    assert '(eq, ":center_faction", "$players_kingdom")' in before
    assert 'severe enough' not in before
    assert '(ge, ":abs_growth", 8)' not in before
    assert '(lt, ":center_health", 35)' not in before
