from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str) -> None:
    assert needle in text, f"Missing expected text: {needle}"


def test_black_khergit_troop_hiring_has_individual_buy_screen_and_custom_prices():
    scripts = read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py")
    join_cost = read("src/scripts/ZA_hardcoded_game_scripts/game_get_join_cost.py")
    dialog = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_hire_pick.py")
    order = read("src/dialogs/_order_dialogs.txt")

    assert_contains(scripts, '"sod_black_khergits_begin_individual_hire_offer"')
    assert_contains(scripts, '"sod_black_khergits_finish_individual_hire_offer"')
    assert_contains(scripts, "$g_sod_black_khergit_hire_horseman_cost")
    assert_contains(scripts, "$g_sod_black_khergit_hire_guard_cost")
    assert_contains(scripts, "(party_add_members, \"p_temp_party\", \"trp_black_khergit_horseman\", \"$g_sod_black_khergit_hire_horsemen\")")
    assert_contains(scripts, "(party_add_members, \"p_temp_party\", \"trp_black_khergit_guard\", \"$g_sod_black_khergit_hire_guards\")")
    assert_contains(scripts, "(party_count_members_of_type, \":horsemen_left\", \"p_temp_party\", \"trp_black_khergit_horseman\")")
    assert_contains(scripts, "(call_script, \"script_sod_black_khergits_choose_relocation_target\")")
    assert_contains(scripts, "(val_add, \"$g_sod_weekly_troops_hired\", \"$g_sod_black_khergit_hire_cost\")")
    assert_contains(scripts, "(val_add, \"$g_sod_weekly_troops_hired\", \":spent\")")
    assert_contains(scripts, "(assign, \"$g_sod_black_khergit_buy_screen_active\", 0)")
    assert_contains(scripts, "(assign, \"$g_sod_black_khergit_hire_horseman_cost\", 0)")
    assert_contains(scripts, "(assign, \"$g_sod_black_khergit_hire_guard_cost\", 0)")

    assert_contains(join_cost, "$g_sod_black_khergit_buy_screen_active")
    assert_contains(join_cost, "(assign, \":join_cost\", \"$g_sod_black_khergit_hire_horseman_cost\")")
    assert_contains(join_cost, "(assign, \":join_cost\", \"$g_sod_black_khergit_hire_guard_cost\")")

    assert_contains(dialog, "script_sod_black_khergits_begin_individual_hire_offer")
    assert_contains(dialog, "(party_get_free_companions_capacity, \":free_capacity\", \"p_main_party\")")
    assert_contains(dialog, "(set_mercenary_source_party, \"p_temp_party\")")
    assert_contains(dialog, "(change_screen_buy_mercenaries)")
    assert_contains(dialog, "script_sod_black_khergits_finish_individual_hire_offer")
    assert_contains(order, "anyone_plyr_black_khergit_khan_hire_pick.py")


def test_black_khergit_prisoners_have_prisoner_and_party_transfer_modes():
    scripts = read("src/scripts/ZY_helper_scripts/sod_black_khergit_horde.py")
    offer = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_black_khergit_khan_prisoner_offer.py")
    prisoner_mode = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_prisoner_confirm.py")
    party_mode = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_prisoner_recruit.py")
    join_cost = read("src/scripts/ZA_hardcoded_game_scripts/game_get_join_cost.py")
    order = read("src/dialogs/_order_dialogs.txt")
    cannot_hire = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_hire_confirm_cannot_pay.py")
    bundle_hire = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_black_khergit_khan_hire_confirm.py")

    assert_contains(scripts, "(party_get_free_prisoners_capacity, \":free_prisoner_capacity\", \"p_main_party\")")
    assert_contains(scripts, "(party_get_free_companions_capacity, \":free_party_capacity\", \"p_main_party\")")
    assert_contains(scripts, "(val_max, \":remaining_offer\", \":free_party_capacity\")")

    assert_contains(prisoner_mode, "script_sod_black_khergits_buy_prisoners")
    assert_contains(prisoner_mode, '(gt, "$g_sod_black_khergit_prisoner_buy_count", 0)')
    assert_contains(prisoner_mode, '(gt, "$g_sod_black_khergit_prisoner_buy_cost", 0)')
    assert_contains(scripts, "(party_add_prisoners, \"p_main_party\", \":prisoner_troop\", \":removed\")")
    assert_contains(scripts, "sod_black_khergits_release_hero_prisoners")

    assert_contains(scripts, '"sod_black_khergits_begin_individual_prisoner_recruit_offer"')
    assert_contains(scripts, '"sod_black_khergits_finish_individual_prisoner_recruit_offer"')
    assert_contains(scripts, "(party_add_members, \"p_temp_party\", \":prisoner_troop\", \":move_count\")")
    assert_contains(scripts, "(party_add_members, \"p_main_party\", \":prisoner_troop\", \":removed\")")
    assert_contains(join_cost, "$g_sod_black_khergit_prisoner_buy_screen_active")
    assert_contains(join_cost, "$g_sod_black_khergit_prisoner_relation_discount")
    assert_contains(scripts, "(assign, \"$g_sod_black_khergit_prisoner_buy_screen_active\", 0)")
    assert_contains(scripts, "(assign, \"$g_sod_black_khergit_prisoner_relation_discount\", 0)")
    assert_contains(scripts, "(assign, \"$g_sod_black_khergit_prisoner_pick_gold_before\", 0)")

    assert_contains(offer, "Take them under guard")
    assert_contains(party_mode, "Those who will take wages can join my ranks")
    assert_contains(party_mode, "(gt, \":player_gold\", 0)")
    assert_contains(party_mode, "(set_mercenary_source_party, \"p_temp_party\")")
    assert_contains(party_mode, "(change_screen_buy_mercenaries)")
    assert_contains(order, "anyone_plyr_black_khergit_khan_prisoner_recruit.py")

    assert_contains(bundle_hire, "(party_get_free_companions_capacity, \":free_capacity\", \"p_main_party\")")
    assert_contains(bundle_hire, "(ge, \":free_capacity\", \":total_hired\")")
    assert_contains(bundle_hire, '(gt, "$g_sod_black_khergit_hire_cost", 0)')
    assert_contains(bundle_hire, '(gt, ":total_hired", 0)')
    assert_contains(cannot_hire, "I do not have room in my ranks")
