from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_effective_faith_helper_exists():
    text = read("src/scripts/ZY_helper_scripts/sod_troop_get_effective_faith.py")
    assert "sod_troop_get_effective_faith" in text
    assert "$g_sod_global_faith" in text
    assert "$g_sod_holy" in text
    assert "reg0" in text


def test_faith_ascension_center_gate_exists():
    text = read("src/scripts/ZY_helper_scripts/sod_troop_can_faith_ascend_at_center.py")
    assert "sod_troop_can_faith_ascend_at_center" in text
    assert "sod_elite_tier_faith" in text
    assert "sod_zealot_min_faith" in text
    assert "sod_faith_ascension_local_min" in text
    assert "slot_center_sod_local_faith" in text
    assert "sod_upgrade_fail_low_faith" in text


def test_core_upgrade_gate_uses_faith_gate():
    text = read("src/scripts/ZY_helper_scripts/sod_troop_can_upgrade_at_center.py")
    assert "script_sod_troop_can_faith_ascend_at_center" in text
    assert "(assign, \":fail_reason\", reg1)" in text


def test_faith_ascension_cost_is_applied():
    helper = read("src/scripts/ZY_helper_scripts/sod_troop_apply_faith_ascension_cost.py")
    assert "sod_faith_ascension_holy_cost" in helper
    assert "$g_sod_holy" in helper

    event = read("src/menus/events/choice_event_holy_1.py")
    assert "script_sod_troop_apply_faith_ascension_cost" in event
    assert "script_sod_troop_get_effective_faith" in event

    menu = read("src/menus/other/sod_upgrade_continue.py")
    assert menu.count("script_sod_troop_apply_faith_ascension_cost") >= 2
    assert menu.count("(neq, reg0, sod_elite_tier_faith)") >= 4


def test_reports_explain_faith_costs():
    text = read("src/scripts/ZY_helper_scripts/sod_describe_elite_doctrine_report.py")
    assert "script_sod_troop_get_effective_faith" in text
    assert "Religious seats" in text
    assert "Each ascension adds holy burden" in text


if __name__ == "__main__":
    test_effective_faith_helper_exists()
    test_faith_ascension_center_gate_exists()
    test_core_upgrade_gate_uses_faith_gate()
    test_faith_ascension_cost_is_applied()
    test_reports_explain_faith_costs()
    print("faith ascension gate checks passed")

