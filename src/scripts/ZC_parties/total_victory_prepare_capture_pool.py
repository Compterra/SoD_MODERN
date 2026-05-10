SCRIPTS = [
("total_victory_prepare_capture_pool",
    [
      # Build the player-facing post-battle capture pool in p_temp_party and
      # peel off the allied share into p_temp_party_2 before the exchange screen.
      (party_clear, "p_temp_party"),
      (party_clear, "p_temp_party_2"),
      (assign, "$g_move_heroes", 0),
      (call_script, "script_party_prisoners_add_wounded_party_companions", "p_temp_party", "p_collective_enemy"),
      (call_script, "script_party_add_party_prisoners", "p_temp_party", "p_collective_enemy"),

      (try_begin),
        (call_script, "script_party_calculate_strength", "p_collective_friends_backup", 0),
        (assign, ":total_initial_strength", reg(0)),
        (gt, ":total_initial_strength", 0),
        (call_script, "script_party_calculate_strength", "p_main_party_backup", 0),
        (assign, ":player_party_initial_strength", reg(0)),
        (store_sub, ":ally_party_initial_strength", ":total_initial_strength", ":player_party_initial_strength"),

        (store_mul, ":ally_share", ":ally_party_initial_strength", 1000),
        (val_div, ":ally_share", ":total_initial_strength"),
        (assign, "$pin_number", ":ally_share"),
        (call_script, "script_move_members_with_ratio", "p_temp_party", "p_temp_party_2"),

        (try_begin),
          (gt, "$g_ally_party", 0),
          (distribute_party_among_party_group, "p_temp_party_2", "$g_ally_party"),
        (try_end),
      (try_end),
  ]),
]
