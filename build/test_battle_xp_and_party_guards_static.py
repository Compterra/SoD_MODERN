from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def assert_before(raw: str, first: str, second: str, label: str = "") -> None:
    assert first in raw, f"missing {first!r} {label}"
    assert second in raw, f"missing {second!r} {label}"
    assert raw.index(first) < raw.index(second), f"{first!r} should appear before {second!r} {label}"


def test_battle_xp_messages_are_aggregated_and_restored() -> None:
    xp_log = read("src/scripts/ZE_encounters/sod_battle_xp_log.py")
    preamble = read("src/mission_templates/_preamble/00_imports.py")
    debrief = read("src/menus/other/continue_05.py")
    map_tick = read("src/triggers/ST01_every_frame/entry_0057.py")
    startup = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")

    for bit in [
        '"sod_battle_xp_log_start"',
        '"sod_battle_xp_log_finish"',
        '(troop_get_xp, "$g_sod_battle_xp_start", "trp_player")',
        '(store_character_level, "$g_sod_battle_level_start", "trp_player")',
        '(assign, "$g_sod_battle_xp_messages_suppressed", 1)',
        "(set_show_messages, 0)",
        "(set_show_messages, 1)",
        "You earned {reg1} experience in the battle",
        "advanced to level {reg2}",
    ]:
        assert bit in xp_log, f"battle XP aggregation missing {bit}"

    assert '(call_script, "script_sod_battle_xp_log_start")' in preamble
    assert_before(
        preamble,
        '(call_script, "script_sod_company_dialogue_process_battle_start_morale")',
        '(call_script, "script_sod_battle_xp_log_start")',
        "in common battle start",
    )
    lead_charge = read("src/mission_templates/0010_lead_charge/lead_charge.py")
    assert_before(
        lead_charge,
        '(call_script, "script_sod_company_dialogue_process_battle_start_morale")',
        '(call_script, "script_sod_battle_xp_log_start")',
        "in lead_charge battle start",
    )
    assert '(call_script, "script_sod_battle_xp_log_finish")' in debrief
    assert '(call_script, "script_sod_battle_xp_log_finish")' in map_tick
    assert_before(
        debrief,
        '(call_script, "script_sod_battle_commander_reset")',
        '(call_script, "script_sod_battle_xp_log_finish")',
        "in battle debrief",
    )
    for bit in [
        '$g_sod_battle_xp_messages_suppressed',
        '$g_sod_battle_xp_start',
        '$g_sod_battle_level_start',
        '$g_sod_battle_xp_gain',
        '$g_sod_battle_level_gain',
    ]:
        assert bit in startup, f"game_start should initialize {bit}"


def test_battle_templates_keep_xp_suppression_active_until_debrief() -> None:
    preamble = read("src/mission_templates/_preamble/00_imports.py")
    assert "common_battle_xp_log_suppression_tick" in preamble
    assert '(eq, "$g_sod_battle_xp_messages_suppressed", 1)' in preamble
    assert "(set_show_messages, 0)" in preamble

    battle_templates = [
        "src/mission_templates/0005_bandits_at_night/bandits_at_night.py",
        "src/mission_templates/0011_village_attack_bandits/village_attack_bandits.py",
        "src/mission_templates/0010_lead_charge/lead_charge.py",
        "src/mission_templates/0013_besiege_inner_battle_castle/besiege_inner_battle_castle.py",
        "src/mission_templates/0012_village_raid/village_raid.py",
        "src/mission_templates/0016_castle_attack_walls_belfry/castle_attack_walls_belfry.py",
        "src/mission_templates/0017_castle_attack_walls_ladder/castle_attack_walls_ladder.py",
        "src/mission_templates/0015_castle_attack_walls_defenders_sally/castle_attack_walls_defenders_sally.py",
        "src/mission_templates/0014_besiege_inner_battle_town_center/besiege_inner_battle_town_center.py",
        "src/mission_templates/0050_custom_battle/custom_battle.py",
        "src/mission_templates/0051_custom_battle_siege/custom_battle_siege.py",
    ]
    for path in battle_templates:
        raw = read(path)
        assert "common_battle_xp_log_suppression_tick" in raw, f"{path} can re-enable XP log spam during battle"
        assert (
            "common_battle_mission_start" in raw
            or '(call_script, "script_sod_battle_xp_log_start")' in raw
        ), f"{path} suppresses XP without starting the battle XP snapshot"


def test_stale_lord_party_ids_are_guarded_before_party_ops() -> None:
    hourly = read("src/scripts/ZI_campaign_ai/sod_hourly_lord_ai_maintenance.py")
    mark = hourly[hourly.index('("sod_hourly_lord_ai_mark_commanders"') :]
    assert_before(
        mark,
        '(party_is_active, ":lord_party")',
        '(party_get_slot, ":commander_party", ":lord_party", slot_party_commander_party)',
        "in commander marker",
    )
    assert_before(
        mark,
        '(party_get_num_companion_stacks, ":commander_stacks", ":commander_party")',
        '(party_stack_get_troop_id, ":commander_troop", ":commander_party", 0)',
        "before reading commander stack",
    )
    assert '(troop_set_slot, ":lord", slot_troop_leaded_party, -1)' in mark
    assert '(party_set_slot, ":lord_party", slot_party_commander_party, -1)' in mark

    avoid = read("src/scripts/ZY_helper_scripts/sod_world_map_trigger_services.py")
    avoid = avoid[avoid.index('("sod_world_map_process_lord_avoid_party_ai"') :]
    assert_before(
        avoid,
        '(party_is_active, ":cur_party")',
        '(party_slot_eq, ":cur_party", slot_party_type, spt_kingdom_hero_party)',
        "in avoid-party AI",
    )

    follow_army = read("src/triggers/ST02_every_hour/entry_0077.py")
    assert_before(
        follow_army,
        '(party_is_active, ":faction_marshall_party")',
        '(store_distance_to_party_from_party, ":dist", ":faction_marshall_party", "p_main_party")',
        "in follow-army quest trigger",
    )


def main() -> None:
    test_battle_xp_messages_are_aggregated_and_restored()
    test_battle_templates_keep_xp_suppression_active_until_debrief()
    test_stale_lord_party_ids_are_guarded_before_party_ops()
    print("battle XP aggregation and party guard static checks passed")


if __name__ == "__main__":
    main()
