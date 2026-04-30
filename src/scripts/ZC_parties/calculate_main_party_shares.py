SCRIPTS = [
("calculate_main_party_shares",
    [
      (assign, ":num_player_party_shares", player_loot_share),
      # Add shares for player's party
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range, ":i_stack", 1, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop", "p_main_party", ":i_stack"),
        (try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),
          (val_add, ":num_player_party_shares", ":stack_size"),
        (else_try),
          (val_add, ":num_player_party_shares", hero_loot_share),
        (try_end),
      (try_end),

      (assign, reg0, ":num_player_party_shares"),
  ]),
]
