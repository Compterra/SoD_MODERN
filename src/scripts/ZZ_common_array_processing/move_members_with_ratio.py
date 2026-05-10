SCRIPTS = [
("move_members_with_ratio",
    [
      (store_script_param_1, ":source_party"), #Source Party_id
      (store_script_param_2, ":target_party"), #Target Party_id
      (party_get_num_prisoner_stacks, ":num_stacks", ":source_party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id,     ":stack_troop", ":source_party", ":stack_no"),
        (party_prisoner_stack_get_size,    ":stack_size", ":source_party", ":stack_no"),
        (store_mul, ":number_to_move", ":stack_size", "$pin_number"),
        (val_div, ":number_to_move", 1000),
        (party_remove_prisoners, ":source_party", ":stack_troop", ":number_to_move"),
        (assign, ":number_moved", reg0),
        (party_add_prisoners, ":target_party", ":stack_troop", ":number_moved"),
      (try_end),
      (party_get_num_companion_stacks, ":num_stacks", ":source_party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop", ":source_party", ":stack_no"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size,    ":stack_size", ":source_party", ":stack_no"),
        (store_mul, ":number_to_move", ":stack_size", "$pin_number"),
        (val_div, ":number_to_move", 1000),
        (party_remove_members, ":source_party", ":stack_troop", ":number_to_move"),
        (assign, ":number_moved", reg0),
        (party_add_members, ":target_party", ":stack_troop", ":number_moved"),
      (try_end),
  ]),
]
