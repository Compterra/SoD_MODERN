from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_ambush_missions_do_not_allow_global_reinforcement_key() -> None:
    city_ambush = read("src/mission_templates/0005_bandits_at_night/bandits_at_night.py")
    village_ambush = read("src/mission_templates/0011_village_attack_bandits/village_attack_bandits.py")
    assert "formations_v" not in city_ambush
    assert "formations_v" not in village_ambush


def test_capture_prisoner_lord_quest_has_dedicated_acceptance_options() -> None:
    order = read("src/dialogs/_order_dialogs.txt")
    accept = "ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told_capture_prisoners.py"
    reject = "ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told_capture_prisoners_02.py"
    generic = "ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told.py"
    assert accept in order
    assert reject in order
    assert order.index(accept) < order.index(generic)
    assert order.index(reject) < order.index(generic)

    accept_text = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told_capture_prisoners.py")
    reject_text = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told_capture_prisoners_02.py")
    generic_accept = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told.py")
    generic_reject = read("src/dialogs/ZB01_lords_politics_and_family/anyone_plyr_lord_mission_told_02.py")
    assert '(eq, "$random_quest_no", "qst_capture_prisoners")' in accept_text
    assert '(eq, "$random_quest_no", "qst_capture_prisoners")' in reject_text
    assert '(neq, "$random_quest_no", "qst_capture_prisoners")' in generic_accept
    assert '(neq, "$random_quest_no", "qst_capture_prisoners")' in generic_reject


def test_construction_reports_sanitize_stale_finished_project_slots() -> None:
    construction = read("src/scripts/ZY_helper_scripts/sod_population_based_construction.py")
    assert '(party_slot_ge, ":center_no", ":building_no", 1)' in construction
    assert '(party_set_slot, ":center_no", slot_center_current_improvement, 0)' in construction

    for path in (
        "src/menus/centers/common/center_manage.py",
        "src/menus/kingdom/fief_available_construction_report.py",
        "src/menus/centers/castle/castle_castle.py",
    ):
        assert "script_sod_ensure_center_construction_state" in read(path)


def test_mercenary_encounter_handles_stale_party_boss_data() -> None:
    troop_name = read("src/scripts/ZH_heroes/store_troop_name.py")
    assert '(neg|is_between, ":troop", 0, "trp_last_troop")' in troop_name
    assert '@unknown captain' in troop_name

    merc_ask = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_party_encounter_mercs_ask.py")
    for token in (
        '(str_store_string, s1, "@an unknown captain")',
        '(str_store_string, s2, "@an unmarked company")',
        '(str_store_string, s3, "@uncertain service")',
        '(is_between, ":troop", 0, "trp_last_troop")',
        '(is_between, ":troop_fac", 0, "fac_factions_end")',
        '(is_between, "$g_encountered_party_faction", 0, "fac_factions_end")',
    ):
        assert token in merc_ask

    merc_attack = read("src/dialogs/ZD01_encounters_battles_and_prisoners/anyone_plyr_party_encounter_mercs_attack.py")
    assert '(party_get_num_companions, ":num_companions", "$g_encountered_party")' in merc_attack
    assert '(gt, ":num_companions", 0)' in merc_attack
    assert '(call_script, "script_sod_safe_leave_encounter")' in merc_attack


def test_quest_start_dialogues_validate_spawn_and_name_parties() -> None:
    guarded_starts = {
        "src/dialogs/ZE01_companions_and_named_npcs/anyone_plyr_kidnapped_girl_quest_brief.py": "qst_kidnapped_girl",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_mission_told_free_clansmen.py": "qst_jotnar_clan_free_clansmen",
        "src/dialogs/ZZ99_misc_dialogs/anyone_plyr_gm_mission_told_free_spy.py": "qst_serpent_host_free_spy",
        "src/dialogs/ZC01_centers_and_economy/anyone_plyr_escort_merchant_caravan_quest_brief.py": "qst_escort_merchant_caravan",
    }
    for path, quest_id in guarded_starts.items():
        raw = read(path)
        assert f'(quest_get_slot, ":quest_target_center", "{quest_id}", slot_quest_target_center)' in raw
        assert '(party_is_active, ":quest_target_center")' in raw
        assert '(party_is_active, "$g_encountered_party")' in raw


if __name__ == "__main__":
    test_ambush_missions_do_not_allow_global_reinforcement_key()
    test_capture_prisoner_lord_quest_has_dedicated_acceptance_options()
    test_construction_reports_sanitize_stale_finished_project_slots()
    test_mercenary_encounter_handles_stale_party_boss_data()
    test_quest_start_dialogues_validate_spawn_and_name_parties()
    print("test_bug_batch_forum_regressions_static: OK")


