SCRIPTS = [
("total_victory_try_ally_thanks",
    [
      (assign, reg0, 0),
      (try_begin),
        (eq, "$thanked_by_ally_leader", 0),
        (gt, "$g_ally_party", 0),
        (party_get_num_companion_stacks, ":num_ally_stacks", "$g_ally_party"),
        (gt, ":num_ally_stacks", 0),

        (assign, "$thanked_by_ally_leader", 1),

        (store_add, ":total_str_without_player", "$g_starting_strength_friends", "$g_starting_strength_enemy_party"),
        (val_sub, ":total_str_without_player", "$g_starting_strength_main_party"),

        (store_sub, ":ally_strength_without_player", "$g_starting_strength_friends", "$g_starting_strength_main_party"),

        (store_mul, ":ally_advantage", ":ally_strength_without_player", 100),
        (val_add, ":total_str_without_player", 1),
        (val_div, ":ally_advantage", ":total_str_without_player"),

        (store_sub, ":enemy_advantage", 100, ":ally_advantage"),

        (store_mul, ":faction_reln_boost", ":enemy_advantage", "$g_starting_strength_enemy_party"),
        (val_div, ":faction_reln_boost", 3000),
        (val_min, ":faction_reln_boost", 4),

        (store_mul, "$g_relation_boost", ":enemy_advantage", ":enemy_advantage"),
        (val_div, "$g_relation_boost", 700),
        (val_clamp, "$g_relation_boost", 0, 20),

        (store_faction_of_party, ":ally_faction", "$g_ally_party"),
        (call_script, "script_change_player_relation_with_faction", ":ally_faction", ":faction_reln_boost"),
        (party_stack_get_troop_id, ":ally_leader", "$g_ally_party"),
        (party_stack_get_troop_dna, ":ally_leader_dna", "$g_ally_party"),
        (try_begin),
          (troop_is_hero, ":ally_leader"),
          (troop_get_slot, ":hero_relation", ":ally_leader", slot_troop_player_relation),
          (assign, ":rel_boost", "$g_relation_boost"),
          (try_begin),
            (lt, ":hero_relation", -5),
            (val_div, ":rel_boost", 3),
          (try_end),
          (call_script, "script_change_player_relation_with_troop", ":ally_leader", ":rel_boost"),
        (try_end),
        (assign, "$talk_context", tc_ally_thanks),
        (call_script, "script_setup_troop_meeting", ":ally_leader", ":ally_leader_dna"),
        (assign, reg0, 1),
      (try_end),
  ]),
]
