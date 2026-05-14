from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT / "src" / "menus" / "centers" / "castle" / "castle_sige_confirm_war.py"


def assert_contains(source: str, needle: str) -> None:
    assert needle in source, f"missing expected siege confirm behavior: {needle}"


def main() -> None:
    source = MENU.read_text(encoding="utf-8")

    assert_contains(source, '"castle_siege_confirm", mnf_enable_hot_keys,')
    assert_contains(source, '("castle_sige_confirm_war", [], "Yes, declare war!"')
    assert_contains(source, '(assign, "$g_player_besiege_town", "$g_encountered_party")')
    assert_contains(source, '(call_script, "script_make_kingdom_hostile_to_player", "$g_encountered_party_faction", -10)')
    assert_contains(source, '(jump_to_menu, "mnu_castle_besiege")')
    assert_contains(source, '("castle_siege_confirm_not", [], "No, this is not the right time.", [(jump_to_menu, "mnu_castle_outside")])')

    for stale in (
        '##          (store_relation, ":relation", "fac_player_supporters_faction", "$g_encountered_party_faction")',
        '##          (assign, ":relation", -40)',
        '##          (call_script, "script_set_player_relation_with_faction", "$g_encountered_party_faction", ":relation")',
        '##          (call_script, "script_update_all_notes")',
    ):
        assert stale not in source, stale

    print("test_siege_confirm_static: OK")


if __name__ == "__main__":
    main()
