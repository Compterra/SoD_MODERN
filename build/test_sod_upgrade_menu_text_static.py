from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def assert_contains(raw: str, token: str) -> None:
    assert token in raw, f"missing token: {token}"


def assert_not_contains(raw: str, token: str) -> None:
    assert token not in raw, f"stale token remains: {token}"


def test_sod_upgrade_menu_text_and_flow_are_clear() -> None:
    town_upgrade = read("src/menus/other/sod_upgrade.py")
    camp_upgrade = read("src/menus/camp/sod_upgrade_camp.py")
    upgrade_continue = read("src/menus/other/sod_upgrade_continue.py")

    assert_contains(town_upgrade, '("sod_upgrade", 0,\n\t"{s98}",')
    assert_contains(town_upgrade, "(str_clear, s98)")
    assert_contains(town_upgrade, "(str_clear, s20)")
    assert_contains(town_upgrade, "(str_store_string_reg, s68, s0)")
    assert_contains(town_upgrade, "(str_store_string_reg, s97, s98)")
    assert_contains(town_upgrade, "(str_store_string_reg, s97, s18)")
    assert_contains(town_upgrade, "troops in your party can be promoted here.{s20}")
    assert_contains(town_upgrade, 'This center can train troops of {s5} and its old {s2} traditions.')
    assert_contains(town_upgrade, 'This center can train troops of {s5}.')
    assert_contains(town_upgrade, '(str_store_string, s18, "@{s68}")')
    assert_contains(town_upgrade, '(str_store_string, s18, "@{s97}, {s68}")')
    assert_not_contains(town_upgrade, '"{s1}"')
    assert_not_contains(town_upgrade, "(str_clear, s1)")
    assert_not_contains(town_upgrade, "@{s1}")
    assert_not_contains(town_upgrade, "@{s18}, {s68}")
    assert_not_contains(town_upgrade, '(str_store_string, s18, "@{s0}")')
    assert_not_contains(town_upgrade, '(str_store_string, s18, "@{s18}, {s0}")')
    assert_not_contains(town_upgrade, "{reg7?This center can train troops")
    assert_not_contains(town_upgrade, "{s5}{reg2?")
    assert_not_contains(town_upgrade, "promoted here.{s19}")
    assert_not_contains(town_upgrade, "(str_clear, s19)")
    assert_not_contains(town_upgrade, "(str_store_string, s19")

    assert_contains(camp_upgrade, '("sod_upgrade_camp", 0,\n\t"{s98}",')
    assert_contains(camp_upgrade, "(str_clear, s98)")
    assert_contains(camp_upgrade, "(str_clear, s20)")
    assert_contains(camp_upgrade, '(assign, "$g_sod_upgrade_center", -1)')
    assert_contains(camp_upgrade, '(str_store_faction_name, s68, ":guild")')
    assert_contains(camp_upgrade, '(str_store_string_reg, s97, s18)')
    assert_contains(camp_upgrade, '(str_store_string, s18, "@{s97}, {s68}")')
    assert_contains(camp_upgrade, "mercenaries in your party can be promoted from camp.{s20}")
    assert_not_contains(camp_upgrade, '"{s1}"')
    assert_not_contains(camp_upgrade, "(str_clear, s1)")
    assert_not_contains(camp_upgrade, "@{s1}")
    assert_not_contains(camp_upgrade, "@{s18}, {s68}")
    assert_not_contains(camp_upgrade, "camp.{s19}")
    assert_not_contains(camp_upgrade, "(str_store_faction_name, s0")
    assert_not_contains(camp_upgrade, "{s0}")
    assert_not_contains(camp_upgrade, "(str_store_string, s19")

    assert_contains(upgrade_continue, '("sod_upgrade_continue", 0,\n\t"{s1}",')
    assert_contains(upgrade_continue, '(assign, ":upgrade_center", "$g_sod_upgrade_center")')
    assert_contains(upgrade_continue, 'script_sod_can_upgrade_troops_here", ":upgrade1", "$g_sod_upgrade_center"')
    assert_contains(upgrade_continue, "(str_store_string, s1, \"@You have {reg4} denars.^^Selected troops: {reg5} {s3}.{s6}{s4}\")")
    assert_contains(upgrade_continue, "Path: {s7} - {s8}.")
    assert_contains(upgrade_continue, '(str_store_string, s68, "@ ({reg0} denars total)")')
    assert_contains(upgrade_continue, '(str_store_string, s68, "@ ({reg0} denars)")')
    assert_contains(upgrade_continue, '(str_store_string, s68, "@ (no charge)")')
    assert_contains(upgrade_continue, '"Promote all {s1} to {s2}{s68}"')
    assert_contains(upgrade_continue, '"Promote five {s1} to {s2}{s68}"')
    assert_contains(upgrade_continue, '"Promote one {s1} to {s2}{s68}"')
    assert_contains(upgrade_continue, "Need {reg0} denars to promote one {s1} to {s2}.")
    assert_contains(upgrade_continue, "This promotion is no longer available here. Return and choose another troop.")
    assert_contains(upgrade_continue, '"Choose another troop."')
    assert_contains(upgrade_continue, '"Leave promotions."')
    assert_not_contains(upgrade_continue, '"Return."')
    assert_contains(upgrade_continue, "performed one soldier at a time")
    assert_not_contains(upgrade_continue, "{reg0?")
    assert_not_contains(upgrade_continue, 'script_sod_get_cost_to_upgrade_troop_at", ":upgrade1", "$g_encountered_party"')
    assert_not_contains(upgrade_continue, "Choose a doctrine path for your {reg5}")

    preamble = read("src/menus/_preamble/00_imports.py")
    assert_contains(preamble, '(assign, ":upgrade_center", "$g_sod_upgrade_center")')
    assert_contains(preamble, '"Promote {s3}."')
    assert_contains(preamble, '"Leave promotions."')
    assert_not_contains(preamble, '"Upgrade {s3}."')
    assert_not_contains(preamble, '"Nevermind."')
    assert_not_contains(preamble, 'script_sod_can_upgrade_troops_here", ":upgrade1", "$g_encountered_party"')


def test_marshal_upgrade_dialog_filters_only_eligible_troops() -> None:
    main_check = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_marshal_upgrade_check.py")
    main_check_again = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_marshal_upgrade_check_again.py")
    main_which = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_plyr_repeat_for_troops_marshal_upgrade_which.py")
    main_options = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_marshal_upgrade_list_options_03.py")
    main_choose_back = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_plyr_marshal_upgrade_choose_07.py")
    main_no_facilities = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_plyr_marshal_upgrade_sorry.py")
    main_no_coin = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_plyr_marshal_upgrade_sorry2.py")
    garrison_check = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_marshal_upgrade_garrison_check.py")
    garrison_check_again = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_marshal_upgrade_garrison_check_again.py")
    garrison_which = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_plyr_repeat_for_troops_marshal_upgrade_garrison_which.py")
    garrison_options = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_marshal_upgrade_garrison_list_options_03.py")
    garrison_choose_back = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_plyr_marshal_upgrade_garrison_choose_07.py")
    garrison_no_facilities = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_plyr_marshal_upgrade_garrison_sorry.py")
    garrison_no_coin = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_marshal_plyr_marshal_upgrade_garrison_sorry2.py")

    for raw in (main_check, main_check_again, garrison_check, garrison_check_again, main_which, garrison_which):
        assert_contains(raw, "slot_troop_sod_upgrade1")
        assert_contains(raw, "slot_troop_sod_upgrade2")
        assert_contains(raw, '(this_or_next|is_between, ":upgrade1", 1, "trp_last_troop")')
        assert_contains(raw, '(is_between, ":upgrade2", 1, "trp_last_troop")')

    for raw in (main_which, garrison_which):
        assert_contains(raw, "(str_store_troop_name_by_count, s68")
        assert_contains(raw, '"{reg1} {s68}"')
        assert_not_contains(raw, '"{s2} {s1}"')

    for raw in (main_options, garrison_options):
        assert_contains(raw, "Promote your {reg1} {s68} into which troop?")
        assert_not_contains(raw, "What should your {reg1} {s1} train to become?")

    assert_contains(main_check, "No troops in your party can be promoted")
    assert_contains(garrison_check, "No garrison troops here can be promoted")
    assert_contains(main_check_again, "Every eligible troop in your party has been promoted")
    assert_contains(garrison_check_again, "Every eligible garrison troop here has been promoted")
    assert_contains(main_choose_back, '"Not now."')
    assert_contains(garrison_choose_back, '"Not now."')
    assert_contains(main_no_facilities, "the right facilities before those men can be promoted")
    assert_contains(garrison_no_facilities, "this garrison needs the right facilities")
    assert_contains(main_no_coin, "until the treasury can cover the promotion")
    assert_contains(garrison_no_coin, "until the treasury can cover the garrison promotion")
    for raw in (main_choose_back, garrison_choose_back, main_no_facilities, main_no_coin, garrison_no_facilities, garrison_no_coin):
        assert_not_contains(raw, "Ahh")
        assert_not_contains(raw, "commision")
        assert_not_contains(raw, "embarrasing")
        assert_not_contains(raw, "....")


if __name__ == "__main__":
    test_sod_upgrade_menu_text_and_flow_are_clear()
    test_marshal_upgrade_dialog_filters_only_eligible_troops()
    print("test_sod_upgrade_menu_text_static: OK")
