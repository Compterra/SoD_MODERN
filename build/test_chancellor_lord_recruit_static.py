from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_chancellor_lord_recruit_action_always_has_escape_option():
    text = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_chancellor_plyr_chancellor_lord_action_02.py")
    assert '[(call_script, "script_sod_chancellor_lord_recruitment_refresh"), (lt, "$territory", 1)]' in text
    assert '[(call_script, "script_sod_chancellor_lord_recruitment_refresh"), (lt, "$lords", 1)]' in text
    assert '[trp_sod_chancellor|plyr, "chancellor_lord_action", []' in text
    assert '"chancellor_talk_again"' in text


def test_chancellor_lord_recruitment_uses_central_scripts():
    prelude = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_chancellor_chancellor_lord_prelude.py")
    action = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_chancellor_plyr_chancellor_lord_action.py")
    recruited_fail = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_chancellor_chancellor_lord_recruited.py")
    recruited_success = read("src/dialogs/ZA02_sod_court_and_strategy/trp_sod_chancellor_chancellor_lord_recruited_02.py")

    assert '(call_script, "script_sod_chancellor_lord_recruitment_refresh")' in prelude
    assert "(try_for_range" not in prelude
    assert '(call_script, "script_sod_chancellor_recruit_homeland_lord")' in action
    assert '[(call_script, "script_sod_chancellor_lord_recruitment_refresh"), (ge, "$lords", 1), (ge, "$territory", 1)]' in action
    assert "troop_set_slot" not in action
    assert '[(lt, "$temp_lord", 1)]' in recruited_fail
    assert '[(ge, "$temp_lord", 1)]' in recruited_success


def test_chancellor_lord_recruitment_script_revalidates_before_recruiting():
    text = read("src/scripts/ZY_helper_scripts/sod_chancellor_lord_recruitment.py")
    assert '("sod_chancellor_lord_recruitment_refresh",' in text
    assert '("sod_chancellor_recruit_homeland_lord",' in text

    recruit_pos = text.index('("sod_chancellor_recruit_homeland_lord",')
    refresh_call = text.index('(call_script, "script_sod_chancellor_lord_recruitment_refresh")', recruit_pos)
    lords_check = text.index('(ge, "$lords", 1)', refresh_call)
    territory_check = text.index('(ge, "$territory", 1)', lords_check)
    occupation_set = text.index('(troop_set_slot, ":lord", slot_troop_occupation, slto_kingdom_hero)', territory_check)
    pending_change_set = text.index('(troop_set_slot, ":lord", slot_troop_change_to_faction, "fac_player_supporters_faction")', territory_check)
    assert refresh_call < lords_check < territory_check < pending_change_set < occupation_set


def test_lord_oath_cash_reset_uses_troop_remove_gold_argument_order():
    text = read("src/dialogs/ZB01_lords_politics_and_family/anyone_loa_swear_oath_done.py")
    assert '(store_troop_gold, ":gold", "$g_talk_troop")' in text
    assert '(troop_remove_gold, "$g_talk_troop", ":gold")' in text
    assert '(troop_remove_gold, ":gold", "$g_talk_troop")' not in text


def test_homeless_lord_daily_handler_skips_pending_faction_changes():
    text = read("src/triggers/ST03_daily/entry_0046.py")
    no_party = '(neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 1)'
    no_pending_change = '(neg|troop_slot_ge, ":troop_no", slot_troop_change_to_faction, 1)'
    faction_read = '(store_troop_faction, ":cur_faction", ":troop_no")'
    positions = [text.index(no_party), text.index(no_pending_change), text.index(faction_read)]
    assert positions == sorted(positions)
