MENUS = [
(
    "join_battle", mnf_enable_hot_keys,
    "You are helping {s2} against {s1}. You have {reg10} troops fit for battle against the enemy's {reg11}.",
    "none",
    [
      (set_background_mesh, "mesh_pic_involve"),

      (str_store_party_name, 1, "$g_enemy_party"),
      (str_store_party_name, 2, "$g_ally_party"),
      # MORDACHAI - use faction names instead of party names
      #(store_faction_of_party, ":enemy_faction", "$g_enemy_party"),
      #(store_faction_of_party, ":ally_faction", "$g_ally_party"),
      #(str_store_faction_name, 1, ":enemy_faction"),
      #(str_store_faction_name, 2, ":ally_faction"),

      (call_script, "script_encounter_calculate_fit"),

      (try_begin),
        (eq, "$new_encounter", 1),
        (assign, "$new_encounter", 0),
        (call_script, "script_encounter_init_variables"),
##          (assign, "$capture_screen_shown", 0),
##          (assign, "$loot_screen_shown", 0),
##          (assign, "$g_battle_result", 0),
##          (assign, "$cant_leave_encounter", 0),
##          (assign, "$last_defeated_hero", 0),
##          (assign, "$last_freed_hero", 0),
##          (call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
##          (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"),
##          (call_script, "script_party_copy", "p_ally_party_backup", "p_collective_ally"),
        (else_try), #second or more turn
          (eq, "$g_leave_encounter", 1),
          (change_screen_return),
        (try_end),

        (try_begin),
          (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
          (assign, ":num_enemy_regulars_remaining", reg(0)),
          (assign, ":enemy_finished", 0),
          (try_begin),
            (eq, "$g_battle_result", 1),
            (eq, ":num_enemy_regulars_remaining", 0), #battle won
            (assign, ":enemy_finished", 1),
          (else_try),
            (eq, "$g_engaged_enemy", 1),
            (le, "$g_enemy_fit_for_battle", 0),
            (ge, "$g_friend_fit_for_battle", 1),
            (assign, ":enemy_finished", 1),
          (try_end),
          (this_or_next|eq, ":enemy_finished", 1),
          (eq, "$g_enemy_surrenders", 1),
          (assign, "$g_next_menu", -1),
          (jump_to_menu, "mnu_total_victory"),
        (else_try),
#          (eq, "$encountered_party_hostile", 1),
          (call_script, "script_party_count_members_with_full_health", "p_collective_friends"),
          (assign, ":ally_num_soldiers", reg(0)),
          (assign, ":battle_lost", 0),
          (try_begin),
            (eq, "$g_battle_result", -1),
            (eq, ":ally_num_soldiers", 0), #battle lost
            (assign, ":battle_lost", 1),
          (try_end),
          (this_or_next|eq, ":battle_lost", 1),
          (eq, "$g_player_surrenders", 1),
        # TODO: Split prisoners to all collected parties.
        # NO Need? Let default battle logic do it for us.
#          (assign, "$g_move_heroes", 0),
#          (call_script, "script_party_add_party_prisoners", "$g_enemy_party", "p_collective_ally"),
#          (call_script, "script_party_prisoners_add_party_companions", "$g_enemy_party", "p_collective_ally"),
        #TODO: Clear all attached allies.
#          (call_script, "script_party_remove_all_companions", "$g_ally_party"),
#          (call_script, "script_party_remove_all_prisoners", "$g_ally_party"),
          (leave_encounter),
          (change_screen_return),
        (try_end),
      ],
      [

        ("join_attack", [
          (neg|troop_is_wounded, "trp_player"),
        ],
        "Charge the enemy.", [
          (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
          (assign, "$g_battle_result", 0),
          (call_script, "script_calculate_renown_value"),
          (call_script, "script_calculate_battle_advantage"),
          (set_battle_advantage, reg0),
          (set_party_battle_mode),
          (set_jump_mission, "mt_lead_charge"),
          (call_script, "script_setup_random_scene"),
          (assign, "$g_next_menu", "mnu_join_battle"),
          (jump_to_menu, "mnu_battle_debrief"),
          (change_screen_mission),
        ]),

        ("join_order_attack", [
#          (gt, "$encountered_party_hostile", 0),
          (call_script, "script_party_count_members_with_full_health", "p_main_party"), (ge, reg(0), 3),
        ],
        "Order your troops to attack with your allies while you stay back.", [
          (party_set_next_battle_simulation_time, "$g_encountered_party", -1),
          (jump_to_menu, "mnu_join_order_attack"),
        ]),

#      ("join_attack", [], "Lead a charge against the enemies", [(set_jump_mission, "mt_charge_with_allies"),
#                                (call_script, "script_setup_random_scene"),
#                                                             (change_screen_mission, 0)]),

      ("join_leave", [], "Leave.",
      [
        (try_begin),
           (neg|troop_is_wounded, "trp_player"),
           (call_script, "script_objectionable_action", tmt_aristocratic, "str_flee_battle"),
           (party_stack_get_troop_id, ":enemy_leader", "$g_enemy_party", 0),
           (call_script, "script_add_log_entry", logent_player_retreated_from_lord, "trp_player", -1, ":enemy_leader", -1),
           (display_message, "@Player retreats from battle", debug_color),
        (try_end),
        (leave_encounter),
        (change_screen_return)
      ]),
    ]
  ),
]
