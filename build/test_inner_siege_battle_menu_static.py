from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT / "src" / "menus" / "other" / "continue_14.py"


def assert_contains(source: str, needle: str) -> None:
    assert needle in source, f"missing expected inner siege behavior: {needle}"


def main() -> None:
    source = MENU.read_text(encoding="utf-8")

    assert_contains(source, '"castle_besiege_inner_battle", mnf_enable_hot_keys')
    assert_contains(source, '(party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_center)')
    assert_contains(source, '(set_jump_mission, "mt_besiege_inner_battle_town_center")')
    assert_contains(source, '(party_get_slot, ":battle_scene", "$g_encountered_party", slot_town_castle)')
    assert_contains(source, '(set_jump_mission, "mt_besiege_inner_battle_castle")')
    assert_contains(source, '(set_party_battle_mode)')
    assert_contains(source, '(jump_to_scene, ":battle_scene")')
    assert_contains(source, '(val_add, "$g_siege_battle_state", 1)')
    assert_contains(source, '(assign, "$g_next_menu", "mnu_castle_besiege_inner_battle")')
    assert_contains(source, '(jump_to_menu, "mnu_battle_debrief")')

    for stale in (
        '##           (call_script, "script_calculate_battle_advantage")',
        '##           (set_battle_advantage, reg0)',
    ):
        assert stale not in source, stale

    print("test_inner_siege_battle_menu_static: OK")


if __name__ == "__main__":
    main()
