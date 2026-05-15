from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def test_serpent_spy_ransom_pay_requires_live_quest_party_and_prisoner() -> None:
    reward = read(
        "src/dialogs/ZC02_townsfolk_and_special_npcs/party_tpl_pt_militia_awaiting_ransom_militia_awaiting_ransom_pay.py"
    )
    player_lines = [
        read(
            "src/dialogs/ZC02_townsfolk_and_special_npcs/party_tpl_pt_militia_awaiting_ransom_plyr_militia_awaiting_ransom_intro_1.py"
        ),
        read("src/dialogs/ZC02_townsfolk_and_special_npcs/anyone_plyr_militia_awaiting_ransom_b2.py"),
    ]

    required = (
        '(check_quest_active, "qst_serpent_host_free_spy")',
        '(neg|check_quest_concluded, "qst_serpent_host_free_spy")',
        '(quest_slot_eq, "qst_serpent_host_free_spy", slot_quest_target_party, "$g_encountered_party")',
        '(party_is_active, "$g_encountered_party")',
    )
    prisoner = '(party_count_prisoners_of_type, ":spy_prisoners", "$g_encountered_party", "trp_sh_spy")'
    prisoner_local = '(party_count_prisoners_of_type, ":spy_prisoners", ":quest_target_party", "trp_sh_spy")'
    remove = '(party_remove_prisoners, ":quest_target_party", "trp_sh_spy", 1)'
    charge = '(call_script, "script_sod_player_charge_gold", ":quest_target_amount")'
    state = '(quest_set_slot, "qst_serpent_host_free_spy", slot_quest_current_state, 1)'
    spawn = '(spawn_around_party, ":quest_target_party", "pt_sh_spy")'

    for raw in player_lines:
        for token in required:
            assert token in raw
    for token in (*required, prisoner, prisoner_local, spawn, remove, charge, state):
        assert token in reward
    assert reward.index(prisoner) < reward.index("You can take the spy now")
    assert reward.index(prisoner_local) < reward.index(spawn) < reward.index(charge) < reward.index(remove) < reward.index(state)


def test_lost_rescue_reports_prepare_ransom_amount_before_text_and_guard_completion() -> None:
    checks = {
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_lost_kidnapped_girl_3.py": (
            "qst_kidnapped_girl",
            "trp_kidnapped_girl",
            "lost kidnapped-girl report could not be completed",
            '(call_script, "script_end_quest", "qst_kidnapped_girl")',
        ),
        "src/dialogs/ZZ99_misc_dialogs/anyone_lost_sh_spy_3.py": (
            "qst_serpent_host_free_spy",
            "trp_sh_spy",
            "lost spy report could not be completed",
            '(call_script, "script_fail_quest", "qst_serpent_host_free_spy")',
        ),
    }

    for rel, (quest, troop, stale_message, terminal) in checks.items():
        raw = read(rel)
        active = f'(check_quest_active, "{quest}")'
        unconcluded = f'(neg|check_quest_concluded, "{quest}")'
        reg8 = f'(quest_get_slot, reg8, "{quest}", slot_quest_target_amount)'
        members = f'(party_count_members_of_type, ":num_members", ":cur_party", "{troop}")'
        prisoners = f'(party_count_prisoners_of_type, ":num_prisoners", ":cur_party", "{troop}")'
        remove_member = f'(party_remove_members, ":cur_party", "{troop}", 1)'
        remove_prisoner = f'(party_remove_prisoners, ":cur_party", "{troop}", 1)'

        for token in (
            active,
            unconcluded,
            reg8,
            members,
            prisoners,
            remove_member,
            remove_prisoner,
            terminal,
            stale_message,
        ):
            assert token in raw
        assert raw.index(reg8) < raw.index("that {reg8} denars")
        assert raw.index(members) < raw.index(prisoners) < raw.index(remove_member) < raw.index(remove_prisoner)
        assert raw.index(remove_prisoner) < raw.index(terminal)


def test_lost_rescue_repayment_options_use_isolated_cached_amounts() -> None:
    kidnap_report = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_lost_kidnapped_girl_3.py")
    spy_report = read("src/dialogs/ZZ99_misc_dialogs/anyone_lost_sh_spy_3.py")
    kidnap_pay = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_lost_kidnapped_girl_4.py")
    spy_pay = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_lost_sh_spy_4.py")
    kidnap_no_pay = read("src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_lost_kidnapped_girl_4_02.py")
    spy_no_pay = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_lost_sh_spy_4_02.py")
    kidnap_debt = read("src/dialogs/ZC01_centers_and_economy/anyone_merchant_quest_about_job_5b_02.py")
    spy_debt = read("src/dialogs/ZC01_centers_and_economy/anyone_merchant_quest_about_job_5b.py")

    cache_kidnap = '(quest_get_slot, "$g_sod_lost_rescue_repayment_amount", "qst_kidnapped_girl", slot_quest_target_amount)'
    cache_spy = '(quest_get_slot, "$g_sod_lost_rescue_repayment_amount", "qst_serpent_host_free_spy", slot_quest_target_amount)'
    charge = '(call_script, "script_sod_player_charge_gold", "$g_sod_lost_rescue_repayment_amount")'
    reset = '(assign, "$g_sod_lost_rescue_repayment_amount", 0)'

    assert cache_kidnap in kidnap_report
    assert cache_spy in spy_report
    for raw in (kidnap_pay, spy_pay):
        assert '(gt, "$g_sod_lost_rescue_repayment_amount", 0)' in raw
        assert '(ge, ":gold", "$g_sod_lost_rescue_repayment_amount")' in raw
        assert charge in raw
        assert reset in raw
        assert "quest_get_slot" not in raw
    assert '"lost_kidnapped_girl_debt"' in kidnap_no_pay
    assert '"lost_sh_spy_debt"' in spy_no_pay
    for raw in (kidnap_no_pay, spy_no_pay):
        assert '(lt, ":gold", "$g_sod_lost_rescue_repayment_amount")' in raw
        assert '"merchant_quest_about_job_5b"' not in raw
    assert '[anyone, "lost_kidnapped_girl_debt"' in kidnap_debt
    assert '[anyone, "lost_sh_spy_debt"' in spy_debt
    assert '$debt_to_merchants_guild' in kidnap_debt
    assert 'player_debt_to_faction' in spy_debt
    assert reset in kidnap_debt
    assert reset in spy_debt


def test_duplicate_npc_followup_states_are_split_for_rescue_and_debt_flows() -> None:
    order = read("src/dialogs/_order_dialogs.txt")
    girl_start = read("src/dialogs/ZA01_startup_and_dispatch/trp_kidnapped_girl_start_02.py")
    slaver_reject_option = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_tell_mission_collect_debt_02.py")
    other_reject_option = read("src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_tell_mission_collect_debt_2_02.py")
    slaver_reject = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_tell_mission_collect_debt_rejected.py")
    other_reject = read("src/dialogs/ZZ99_misc_dialogs/anyone_gm_tell_mission_collect_debt_rejected_02.py")

    assert "trp_kidnapped_girl_start_03.py" not in order
    for token in (
        '(check_quest_active, "qst_kidnapped_girl")',
        '(neg|check_quest_concluded, "qst_kidnapped_girl")',
        '(quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 3)',
    ):
        assert token in girl_start

    assert '"gm_tell_mission_collect_debt_rejected_slavers"' in slaver_reject_option
    assert '"gm_tell_mission_collect_debt_rejected_other"' in other_reject_option
    assert '[anyone, "gm_tell_mission_collect_debt_rejected_slavers"' in slaver_reject
    assert '[anyone, "gm_tell_mission_collect_debt_rejected_other"' in other_reject
