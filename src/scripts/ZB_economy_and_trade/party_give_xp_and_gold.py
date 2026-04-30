SCRIPTS = [
("party_give_xp_and_gold",
    [
      (store_script_param_1, ":enemy_party"), #Party_id

      (call_script, "script_calculate_main_party_shares"),
      (assign, ":num_player_party_shares", reg0),

      #      (assign, ":num_ally_shares", reg1),
      #     (store_add, ":num_total_shares",  ":num_player_party_shares", ":num_ally_shares"),

      (assign, ":total_gain", 0),
      (party_get_num_companion_stacks, ":num_stacks", ":enemy_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop", ":enemy_party", ":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size", ":enemy_party", ":i_stack"),
        (store_character_level, ":level", ":stack_troop"),
        (store_add, ":gain", ":level", 10),
        (val_mul, ":gain", ":gain"),
        (val_div, ":gain", 10),
        (store_mul, ":stack_gain", ":gain", ":stack_size"),
        (val_add, ":total_gain", ":stack_gain"),
      (try_end),

      (val_mul, ":total_gain", "$g_strength_contribution_of_player"),
      (val_div, ":total_gain", 100),

      (val_min, ":total_gain", 40000), #eliminate negative results


      #      (store_mul, ":player_party_xp_gain", ":total_gain", ":num_player_party_shares"),
      #      (val_div, ":player_party_xp_gain", ":num_total_shares"),

      (assign, ":player_party_xp_gain", ":total_gain"),

      (store_random_in_range, ":r", 50, 100),
      (val_mul, ":player_party_xp_gain", ":r"),
      (val_div, ":player_party_xp_gain", 100),

      (party_add_xp, "p_main_party", ":player_party_xp_gain"),

      (store_mul, ":player_gold_gain", ":total_gain", player_loot_share),
      (val_min, ":player_gold_gain", 60000), #eliminate negative results
      (store_random_in_range, ":r", 50, 100),
      (val_mul, ":player_gold_gain", ":r"),
      (val_div, ":player_gold_gain", 100),
      (val_div, ":player_gold_gain", ":num_player_party_shares"),

      #add gold now
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop", "p_main_party", ":i_stack"),
        (try_begin),
          (troop_is_hero, ":stack_troop"),
          (call_script, "script_troop_add_gold", ":stack_troop", ":player_gold_gain"),
        (try_end),
      (try_end),

      #Add morale
      (assign, ":morale_gain", ":total_gain"),
      (val_div, ":morale_gain", ":num_player_party_shares"),
      (call_script, "script_change_player_party_morale", ":morale_gain"),
  ]),
]
