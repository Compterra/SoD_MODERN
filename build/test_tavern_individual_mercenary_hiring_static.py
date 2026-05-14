from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str) -> None:
    assert needle in text, f"Missing expected text: {needle}"


def assert_not_contains(text: str, needle: str) -> None:
    assert needle not in text, f"Unexpected text: {needle}"


def test_tavern_mercenary_dialog_order_includes_individual_hire_flow():
    order = read("src/dialogs/_order_dialogs.txt")

    expected = [
        "ZC02_townsfolk_and_special_npcs/anyone_plyr_mercenary_tavern_talk.py",
        "ZC02_townsfolk_and_special_npcs/anyone_plyr_mercenary_tavern_talk_02.py",
        "ZC02_townsfolk_and_special_npcs/anyone_plyr_mercenary_tavern_talk_pick.py",
        "ZC02_townsfolk_and_special_npcs/anyone_mercenary_tavern_talk_hire.py",
        "ZC02_townsfolk_and_special_npcs/anyone_mercenary_tavern_talk_hire_pick.py",
        "ZC02_townsfolk_and_special_npcs/anyone_mercenary_tavern_talk_hire_pick_return.py",
        "ZC02_townsfolk_and_special_npcs/anyone_plyr_mercenary_tavern_talk_hire_pick_done.py",
        "ZC02_townsfolk_and_special_npcs/anyone_mercenary_tavern_talk_hire_pick_finish.py",
    ]
    positions = [order.index(item) for item in expected]
    assert positions == sorted(positions)


def test_direct_hire_preserves_leftover_town_stock():
    hire = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_mercenary_tavern_talk_hire.py")

    assert_contains(hire, "(party_get_slot, \":mercenary_amount\", \"$g_encountered_party\", slot_center_mercenary_troop_amount)")
    assert_contains(hire, "(val_sub, \":mercenary_amount\", \"$temp\")")
    assert_contains(hire, "(party_set_slot, \"$g_encountered_party\", slot_center_mercenary_troop_amount, \":mercenary_amount\")")
    assert_not_contains(hire, "(party_set_slot, \"$g_encountered_party\", slot_center_mercenary_troop_amount, 0)")


def test_individual_hire_uses_temp_party_and_reconciles_leftovers():
    pick = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_mercenary_tavern_talk_hire_pick.py")
    done = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_mercenary_tavern_talk_hire_pick_done.py")
    finish = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_mercenary_tavern_talk_hire_pick_finish.py")

    assert_contains(pick, "(party_clear, \"p_temp_party\")")
    assert_contains(pick, "(party_add_members, \"p_temp_party\", \":mercenary_troop\", \":mercenary_amount\")")
    assert_contains(pick, "(set_mercenary_source_party, \"p_temp_party\")")
    assert_contains(pick, "(change_screen_buy_mercenaries)")
    assert_contains(pick, "$g_sod_tavern_merc_pick_start_amount")
    assert_contains(pick, "$g_sod_tavern_merc_pick_gold_before")

    assert_contains(done, "(party_get_num_companions, \":remaining\", \"p_temp_party\")")
    assert_contains(done, "(store_sub, \":hired\", \":starting_amount\", \":remaining\")")
    assert_contains(done, "(party_set_slot, \"$g_encountered_party\", slot_center_mercenary_troop_amount, \":remaining\")")
    assert_contains(done, "(val_add, \"$g_sod_weekly_troops_hired\", \":spent\")")
    assert_contains(done, "(val_sub, \":pop\", \":hired\")")

    assert_contains(finish, "(party_clear, \"p_temp_party\")")
    assert_contains(finish, "(assign, \"$g_sod_tavern_merc_pick_start_amount\", 0)")
    assert_contains(finish, "(assign, \"$g_sod_tavern_merc_pick_gold_before\", 0)")
