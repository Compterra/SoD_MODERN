from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_boar_clan_toll_is_persisted_and_clamped_when_demanded():
    dialog = read("src/dialogs/ZZ99_misc_dialogs/anyone_boar_clan_introduce.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_boar_clan_encounter.py")
    assert '(call_script, "script_sod_boar_clan_prepare_encounter")' in dialog
    assert '(store_party_size, ":toll", ":party_no")' in helper
    assert '(val_mul, ":toll", 10)' in helper
    assert '(val_clamp, ":toll", 1, 1001)' in helper
    assert '(assign, "$g_sod_boar_toll_amount", reg0)' in helper


def test_boar_clan_payment_never_spends_raw_register_value():
    text = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_boar_clan_talk_03.py")
    remove = '(call_script, "script_sod_player_charge_gold", reg5)'
    first_load = '(assign, reg5, "$g_sod_boar_toll_amount")'
    clamp = "(val_clamp, reg5, 1, 1001)"
    assert first_load in text
    assert clamp in text
    assert remove in text
    assert text.index(first_load) < text.index(clamp) < text.index(remove)
    assert "(troop_remove_gold, \"trp_player\"" not in text


def test_boar_clan_toll_is_cleared_after_barter():
    text = read("src/dialogs/ZZ99_misc_dialogs/anyone_boar_clan_barter.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_boar_clan_encounter.py")
    assert '(call_script, "script_sod_boar_clan_grant_toll_passage")' in text
    assert '(assign, "$g_sod_boar_toll_amount", 0)' in helper


def test_boar_clan_hire_price_is_persisted_and_clamped():
    dialog = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_boar_clan_recruit_2.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_boar_clan_encounter.py")
    assert '(call_script, "script_sod_boar_clan_prepare_hire_offer")' in dialog
    assert '(val_clamp, ":total_cost", 1, 20001)' in helper
    assert '(assign, "$g_sod_boar_hire_cost", reg0)' in helper
    assert '(assign, reg5, reg0)' in helper


def test_boar_clan_hire_payment_never_spends_raw_register_value():
    text = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_boar_clan_recruit_3.py")
    helper = read("src/scripts/ZY_helper_scripts/sod_boar_clan_encounter.py")
    remove = '(call_script, "script_sod_player_charge_gold", ":hire_cost")'
    first_load = '(assign, reg5, "$g_sod_boar_hire_cost")'
    clamp = "(val_clamp, reg5, 1, 20001)"
    preserve = '(assign, ":hire_cost", reg5)'
    assert first_load in text
    assert clamp in text
    assert preserve in text
    assert remove in text
    assert text.index(first_load) < text.index(clamp) < text.index(preserve) < text.index(remove)
    assert '(assign, "$g_sod_boar_hire_cost", 0)' in text
    assert '(call_script, "script_sod_boar_clan_convert_to_player_mercenaries")' in text
    assert '(spawn_around_party, "$g_encountered_party", "pt_player_mercenaries")' in helper
    assert '(gt, ":mercs", 0)' in helper
    assert helper.index('(gt, ":mercs", 0)') < helper.index('(remove_party, "$g_encountered_party")')


def test_boar_clan_hire_price_is_cleared_when_refused():
    text = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_boar_clan_recruit_3_02.py")
    assert '(assign, "$g_sod_boar_hire_cost", 0)' in text
