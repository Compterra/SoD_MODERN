from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT / "src" / "menus" / "centers" / "castle" / "talk_to_siege_commander.py"


def assert_contains(source: str, needle: str) -> None:
    assert needle in source, f"missing expected siege commander behavior: {needle}"


def main() -> None:
    source = MENU.read_text(encoding="utf-8")

    assert_contains(source, '"besiegers_camp_with_allies", mnf_enable_hot_keys,')
    assert_contains(source, '(call_script, "script_party_wound_all_members", "$g_enemy_party")')
    assert_contains(source, '(party_collect_attachments_to_party, "$g_enemy_party", "p_collective_enemy")')
    assert_contains(source, '(assign, "$g_next_menu", "mnu_castle_taken_by_friends")')
    assert_contains(source, '(jump_to_menu, "mnu_total_victory")')
    assert_contains(source, '(assign, "$g_siege_final_menu", "mnu_besiegers_camp_with_allies")')
    assert_contains(source, '(assign, "$g_siege_battle_state", 1)')
    assert_contains(source, '(assign, "$g_next_menu", "mnu_castle_besiege_inner_battle")')
    assert_contains(source, '(jump_to_menu, "mnu_battle_debrief")')

    for stale in (
        '##          (assign, "$g_next_menu", -1)',
        '##           (assign, "$g_next_menu", "mnu_besiegers_camp_with_allies")',
    ):
        assert stale not in source, stale

    print("test_siege_commander_menu_static: OK")


if __name__ == "__main__":
    main()
