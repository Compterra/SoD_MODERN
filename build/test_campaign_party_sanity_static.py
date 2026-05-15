from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def main():
    helper = read("src/scripts/ZY_helper_scripts/sod_campaign_party_sanity.py")
    trigger = read("src/triggers/ST02_every_hour/entry_0164.py")

    required_helper_bits = [
        '"sod_campaign_party_sanity"',
        "spt_kingdom_hero_party",
        "spt_ai_mercenaries",
        "spt_mercenary_lord_party",
        "slot_party_boss",
        "slot_party_commander_party",
        "party_set_faction",
        "slot_party_ignore_player_until",
        "party_ignore_player",
        "fac_neutral",
        "fac_commoners",
    ]
    for bit in required_helper_bits:
        assert bit in helper, f"missing campaign party sanity helper coverage: {bit}"

    assert "set_show_messages, 1" in trigger, "hourly message leak reset was removed"
    assert "script_sod_campaign_party_sanity" in trigger, "hourly trigger does not call campaign party sanity helper"

    startup = read("src/scripts/ZA_hardcoded_game_scripts/game_start.py")
    initial_party = read("src/scripts/ZC_parties/sod_initialize_party.py")
    start_phase_2 = read("src/menus/0000_hardcoded_mb1011/start_phase_2.py")
    trigger_order = read("src/triggers/_order_simple_triggers.txt")
    icon_trigger = read("src/triggers/ST01_every_frame/entry_0057.py")
    finisher_trigger = read("src/triggers/ST01_every_frame/entry_0169.py")
    hourly_custom_banner = read("src/triggers/ST02_every_hour/entry_0127.py")
    world_map_services = read("src/scripts/ZY_helper_scripts/sod_world_map_trigger_services.py")
    banner_selection = read("src/presentations/0002_banner_selection/banner_selection.py")
    custom_banner = read("src/presentations/0003_custom_banner/custom_banner.py")
    morale = read("src/scripts/ZC_parties/get_player_party_morale_values.py")
    reset_name = read("src/scripts/ZA_hardcoded_game_scripts/game_reset_player_party_name.py")
    companion_count = read("src/scripts/ZH_heroes/get_count_of_companions.py")
    strength = read("src/scripts/ZC_parties/party_calculate_strength.py")

    assert '(assign, "$g_sod_main_party_setup_pending", 0)' in startup
    assert '(call_script, "script_sod_try_finish_initial_party_after_creation")' not in startup
    assert '(call_script, "script_sod_try_finish_initial_party_after_creation")' not in start_phase_2
    assert '(assign, "$g_sod_main_party_setup_pending", 0)' in initial_party
    assert '(call_script, "script_sod_apply_initial_party_members")' in initial_party
    assert '(party_relocate_near_party, "p_main_party"' not in startup
    assert '(party_set_name, "p_main_party", s5)' not in startup
    assert '(party_relocate_near_party, "p_main_party"' in initial_party
    assert '(party_set_name, "p_main_party", s5)' in initial_party
    assert '(call_script, "script_sod_refresh_player_map_icon_if_dirty")' in icon_trigger
    assert "(map_free)" in world_map_services
    assert '(party_set_icon, "p_main_party", ":new_icon")' in initial_party
    assert '(main_party_has_troop, "trp_player")' in initial_party
    assert '(call_script, "script_sod_apply_initial_party_members")' in initial_party
    assert "$g_sod_initial_party_members_pending" in initial_party
    assert '(assign, "$g_sod_initial_party_members_pending", 0)' in initial_party
    assert '"sod_try_finish_initial_party_after_creation"' in initial_party
    assert "ST01_every_frame/entry_0169.py" in trigger_order
    assert '(call_script, "script_sod_finish_initial_party_world_setup")' in finisher_trigger
    assert "(map_free)" in finisher_trigger
    assert "(map_free)" in initial_party
    assert '(call_script, "script_sod_world_map_refresh_custom_banner_parties")' in hourly_custom_banner
    assert "try_for_parties" not in hourly_custom_banner
    for bit in [
        '"sod_world_map_refresh_custom_banner_parties"',
        "script_sod_apply_player_banner_map_icon",
        "$g_sod_custom_banner_last_world_icon",
        "$g_sod_custom_banner_next_world_refresh_hour",
        '(store_add, "$g_sod_custom_banner_next_world_refresh_hour", ":cur_hours", 24)',
        '(party_is_active, ":cur_party")',
        "script_cf_is_patrol",
        '(party_set_banner_icon, ":cur_party", ":flag_icon")',
        '(party_set_banner_icon, ":cur_center", ":flag_icon")',
    ]:
        assert bit in world_map_services, f"missing custom-banner world refresh guard: {bit}"
    refresh_block = world_map_services[
        world_map_services.index('("sod_world_map_refresh_custom_banner_parties"') :
        world_map_services.index('("sod_world_map_process_lord_avoid_party_ai"', world_map_services.index('("sod_world_map_refresh_custom_banner_parties"'))
    ]
    assert refresh_block.index("(try_begin)") < refresh_block.index('(eq, "$g_custom_banner", 1)')
    stuck_party_trigger = read("src/triggers/ST03_daily/entry_0148.py")
    assert '(call_script, "script_sod_world_map_nudge_stuck_parties")' in stuck_party_trigger
    assert "try_for_parties" not in stuck_party_trigger
    for bit in [
        '"sod_world_map_nudge_stuck_parties"',
        '(try_for_parties, ":cur_party")',
        '(neg|is_between, ":cur_party", 0, "p_spawn_points_end")',
        '(party_get_attached_to, ":attached", ":cur_party")',
        '(party_get_battle_opponent, ":opponent", ":cur_party")',
        '(party_slot_eq, ":cur_party", slot_party_old_x, ":x")',
        '(party_slot_eq, ":cur_party", slot_party_old_y, ":y")',
        "(map_get_land_position_around_position, pos1, pos0, 1)",
        '(party_set_position, ":cur_party", pos1)',
    ]:
        assert bit in world_map_services, f"missing stuck-party nudge guard: {bit}"
    for path, raw in (
        ("banner_selection.py", banner_selection),
        ("custom_banner.py", custom_banner),
        ("sod_world_map_trigger_services.py", world_map_services),
    ):
        assert '(party_set_banner_icon, "p_main_party"' not in raw, (
            f"{path} should route main-party banner changes through the deferred startup helper"
        )
        assert "script_sod_apply_player_banner_map_icon" in raw, (
            f"{path} should use the deferred main-party banner helper"
        )
    for path, raw in (
        ("get_player_party_morale_values.py", morale),
        ("sod_initialize_party.py", initial_party),
        ("game_reset_player_party_name.py", reset_name),
        ("get_count_of_companions.py", companion_count),
    ):
        assert '(main_party_has_troop, "trp_player")' in raw, (
            f"{path} should use the player-party readiness gate for startup-era p_main_party access"
        )
    assert '(party_is_active, ":party")' in strength, (
        "party_calculate_strength.py should guard arbitrary party ids before reading stacks"
    )

    print("campaign party sanity static checks passed")


if __name__ == "__main__":
    main()
