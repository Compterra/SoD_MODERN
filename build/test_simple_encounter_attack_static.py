from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT / "src" / "menus" / "0000_hardcoded_mb1011" / "simple_encounter.py"


def assert_contains(source: str, needle: str) -> None:
    assert needle in source, f"missing expected simple encounter behavior: {needle}"


def main() -> None:
    source = MENU.read_text(encoding="utf-8")

    assert_contains(source, '"simple_encounter", mnf_enable_hot_keys|mnf_scale_picture')
    assert_contains(source, '("encounter_attack", [')
    assert_contains(source, '(eq, "$encountered_party_friendly", 0)')
    assert_contains(source, '(call_script, "script_cf_sod_battle_commander_can_start")')
    assert_contains(source, '(assign, "$g_battle_result", 0)')
    assert_contains(source, '(assign, "$g_engaged_enemy", 1)')
    assert_contains(source, '(call_script, "script_calculate_renown_value")')
    assert_contains(source, '(call_script, "script_calculate_battle_advantage")')
    assert_contains(source, '(set_battle_advantage, reg0)')
    assert_contains(source, '(assign, "$g_next_menu", "mnu_simple_encounter")')
    assert_contains(source, '(jump_to_menu, "mnu_battle_debrief")')

    for stale in (
        "##         (store_troop_health, reg(5))",
        "##         (ge, reg(5), 5)",
    ):
        assert stale not in source, stale

    print("test_simple_encounter_attack_static: OK")


if __name__ == "__main__":
    main()
