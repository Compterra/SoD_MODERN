from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str) -> None:
    assert needle in text, f"Missing expected text: {needle}"


def assert_not_contains(text: str, needle: str) -> None:
    assert needle not in text, f"Unexpected text: {needle}"


def test_ransom_broker_guard_refill_uses_missing_space_not_negative_space():
    text = read("src/scripts/ZH_heroes/add_merc_troops.py")

    assert_contains(text, '(store_party_size,":size","p_sod_merc_rb")')
    assert_contains(text, '(lt, ":size", 15)')
    assert_contains(text, '(store_sub, ":dif", 15, ":size")')
    assert_not_contains(text, '(store_sub, ":dif", ":size", 15)')
    assert_contains(text, '(party_add_members, "p_sod_merc_rb", "trp_watchman", ":rand")')
    assert_contains(text, '(party_add_members, "p_sod_merc_rb", "trp_caravan_guard", ":rand")')


def test_tavernkeeper_local_hires_are_stock_gated_and_track_actual_spend():
    option = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_tavernkeeper_talk_04.py")
    hire = read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_tavernkeeper_buy_peasants_02.py")

    assert_contains(option, '(gt, "$tavernkeeper_party", 0)')
    assert_contains(option, '(store_party_size, ":available", "$tavernkeeper_party")')
    assert_contains(option, '(gt, ":available", 0)')

    assert_contains(hire, '(set_mercenary_source_party, "$tavernkeeper_party")')
    assert_contains(hire, '(store_troop_gold, ":before", "trp_player")')
    assert_contains(hire, '(change_screen_buy_mercenaries)')
    assert_contains(hire, '(store_troop_gold, ":after", "trp_player")')
    assert_contains(hire, '(val_add, "$g_sod_weekly_troops_hired", reg0)')
    assert_contains(hire, "They are not guild men")


def test_guild_master_individual_hire_paths_track_actual_spend_and_require_stock():
    paths = [
        "src/dialogs/ZZ99_misc_dialogs/anyone_gm_hire_single.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_gm_hire_single_02.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_gm_hire_elite.py",
        "src/dialogs/ZZ99_misc_dialogs/anyone_gm_hire_elite_02.py",
    ]

    for rel in paths:
        text = read(rel)
        assert_contains(text, '(store_party_size, ":available"')
        assert_contains(text, '(gt, ":available", 0)')
        assert_contains(text, '(store_troop_gold, ":before", "trp_player")')
        assert_contains(text, '(change_screen_buy_mercenaries)')
        assert_contains(text, '(store_troop_gold, ":after", "trp_player")')
        assert_contains(text, '(store_sub, reg0, ":before", ":after")')
        assert_contains(text, '(val_add, "$g_sod_weekly_troops_hired", reg0)')
