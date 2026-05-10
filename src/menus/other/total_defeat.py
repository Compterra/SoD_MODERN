MENUS = [
(
    "total_defeat", 0,
    "You shouldn't be reading this...",
    "none",
    [
        (play_track, "track_captured", 1),
          (call_script, "script_sod_company_accounts_record_battle_defeat"),
           # Free prisoners
          (party_get_num_prisoner_stacks, ":num_prisoner_stacks", "p_main_party"),
          (try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
            (party_prisoner_stack_get_troop_id, ":stack_troop", "p_main_party", ":stack_no"),
            (troop_is_hero, ":stack_troop"),
            (call_script, "script_remove_troop_from_prison", ":stack_troop"),
          (try_end),

          (try_begin),
            (party_stack_get_troop_id, ":captor_troop", "$g_enemy_party", 0),
            (is_between, ":captor_troop", kingdom_heroes_begin, kingdom_heroes_end),
            (call_script, "script_sod_artifact_capture_spoils", ":captor_troop", "trp_player"),
          (try_end),

          (try_begin),
            (gt, "$g_enemy_party", 0),
            (party_is_active, "$g_enemy_party"),
            (party_slot_ge, "$g_enemy_party", slot_party_sod_looter_raid_state, sod_looter_raid_state_moving_to_target),
            (call_script, "script_sod_looter_handle_player_defeat_near_village_raid", "$g_enemy_party"),
          (try_end),

          (call_script, "script_loot_player_items", "$g_enemy_party"),

          (assign, "$g_move_heroes", 0),
          (party_clear, "p_temp_party"),
          (call_script, "script_party_add_party_prisoners", "p_temp_party", "p_main_party"),
          (call_script, "script_party_prisoners_add_party_companions", "p_temp_party", "p_main_party"),
          (distribute_party_among_party_group, "p_temp_party", "$g_enemy_party"),

          (call_script, "script_sod_companion_retinue_handle_player_defeat"),
          (call_script, "script_party_remove_all_companions", "p_main_party"),
          (assign, "$g_move_heroes", 1),
          (call_script, "script_party_remove_all_prisoners", "p_main_party"),

          (val_add, "$g_total_defeats", 1),
          (try_begin),
            (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
            (faction_get_slot, ":weariness", "$players_kingdom", slot_faction_diplomacy_war_weariness),
            (val_add, ":weariness", 4),
            (val_clamp, ":weariness", 0, 101),
            (faction_set_slot, "$players_kingdom", slot_faction_diplomacy_war_weariness, ":weariness"),
          (try_end),

          (try_begin),
            (store_random_in_range, ":random_no", 0, 100),
            (ge, ":random_no", "$g_player_luck"),
            (jump_to_menu, "mnu_permanent_damage"),
          (else_try),
            (try_begin),
              (eq, "$g_next_menu", -1),
              (leave_encounter),
              (change_screen_return),
            (else_try),
              (jump_to_menu, "$g_next_menu"),
            (try_end),
          (try_end),
          (try_begin),
            (gt, "$g_ally_party", 0),
            (call_script, "script_party_wound_all_members", "$g_ally_party"),
          (try_end),

#Troop commentary changes begin
          (party_get_num_companion_stacks, ":num_stacks", "p_encountered_party_backup"),
          (try_for_range, ":stack_no", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", "p_encountered_party_backup", ":stack_no"),
            (is_between, ":stack_troop", kingdom_heroes_begin, kingdom_heroes_end),
            (store_troop_faction, ":victorious_faction", ":stack_troop"),
            (call_script, "script_add_log_entry", logent_player_defeated_by_lord, "trp_player", -1, ":stack_troop", ":victorious_faction"),
          (try_end),
#Troop commentary changes end

      ],
    []
  ),
]
