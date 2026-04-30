SCRIPTS = [
("encounter_init_variables",
    [
      (assign, "$capture_screen_shown", 0),
      (assign, "$loot_screen_shown", 0),
      (assign, "$thanked_by_ally_leader", 0),
      (assign, "$g_battle_result", 0),
      (assign, "$cant_leave_encounter", 0),
      (assign, "$cant_talk_to_enemy", 0),
      (assign, "$last_defeated_hero", 0),
      (assign, "$last_freed_hero", 0),

      (call_script, "script_encounter_calculate_fit"),
      (call_script, "script_party_copy", "p_main_party_backup", "p_main_party"),
      (call_script, "script_party_calculate_strength", "p_main_party", 0),
      (assign, "$g_starting_strength_main_party", reg0),
      (call_script, "script_party_copy", "p_encountered_party_backup", "p_collective_enemy"),
      (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
      (assign, "$g_starting_strength_enemy_party", reg0),
      #      (assign, "$g_starting_strength_ally_party", 0),
      (assign, "$g_strength_contribution_of_player", 100),

      (call_script, "script_party_copy", "p_collective_friends_backup", "p_collective_friends"),
      (call_script, "script_party_calculate_strength", "p_collective_friends", 0),
      (assign, "$g_starting_strength_friends", reg0),

      (store_mul, "$g_strength_contribution_of_player", "$g_starting_strength_main_party", 100), # reduce contribution if we are helping someone.
      (val_div, "$g_strength_contribution_of_player", "$g_starting_strength_friends"),

      #      (try_begin),
      #        (gt, "$g_ally_party", 0),
      #        (call_script, "script_party_copy", "p_ally_party_backup", "p_collective_ally"),
      #        (call_script, "script_party_calculate_strength", "p_collective_ally"),
      #        (assign, "$g_starting_strength_ally_party", reg0),
      #        (store_add, ":starting_strength_factor_combined", "$g_starting_strength_ally_party", "$g_starting_strength_main_party"),
      #         (store_mul, "$g_strength_contribution_of_player", "$g_starting_strength_main_party", 80), #reduce contribution if we are helping someone.
      #        (val_div, "$g_strength_contribution_of_player", ":starting_strength_factor_combined"),
      #      (try_end),
  ]),
]
