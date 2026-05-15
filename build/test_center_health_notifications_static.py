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
    assert '(str_store_party_name, s68, ":center_no")' in before
    assert "{s0} suffers an unusual health setback" not in raw


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
    report_gate_idx = raw.rfind('(eq, ":should_report_population_change", 1)', 0, message_idx)
    threshold_idx = raw.rfind('(ge, ":abs_growth", 20)', 0, report_gate_idx)
    hide_idx = raw.rfind('(eq, "$g_sod_hide_messages", 0)', 0, report_gate_idx)
    assert threshold_idx >= 0
    assert threshold_idx < hide_idx < report_gate_idx < message_idx
    before = raw[threshold_idx:message_idx]
    assert '(party_slot_eq, ":center_no", slot_town_lord, "trp_player")' in before
    assert '(eq, ":center_faction", "$players_kingdom")' in before
    report_branch = raw[report_gate_idx:message_idx]
    assert 'severe enough' not in report_branch


def test_weekly_village_population_reports_only_player_controlled_centers() -> None:
    raw = read("src/triggers/ST04_weekly/entry_0102.py")
    message_idx = raw.find("Word reaches you from {s1}")
    assert message_idx >= 0
    report_gate_idx = raw.rfind('(eq, ":should_report_population_change", 1)', 0, message_idx)
    threshold_idx = raw.rfind('(ge, ":abs_growth", 8)', 0, report_gate_idx)
    hide_idx = raw.rfind('(eq, "$g_sod_hide_messages", 0)', 0, report_gate_idx)
    assert threshold_idx >= 0
    assert threshold_idx < hide_idx < report_gate_idx < message_idx
    before = raw[threshold_idx:message_idx]
    assert '(party_slot_eq, ":center_no", slot_town_lord, "trp_player")' in before
    assert '(eq, ":center_faction", "$players_kingdom")' in before
    report_branch = raw[report_gate_idx:message_idx]
    assert 'severe enough' not in report_branch
