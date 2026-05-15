SCRIPTS = [
("party_add_party_prisoners",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (try_begin),
        (gt, ":target_party", 0),
        (party_is_active, ":target_party"),
        (gt, ":source_party", 0),
        (party_is_active, ":source_party"),
        (party_get_num_prisoner_stacks, ":num_stacks", ":source_party"),
        (try_for_range, ":stack_no", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id,     ":stack_troop", ":source_party", ":stack_no"),
          (neg|troop_is_hero, ":stack_troop"),
          (party_prisoner_stack_get_size,         ":stack_size", ":source_party", ":stack_no"),
          (party_add_members, ":target_party", ":stack_troop", ":stack_size"),
        (try_end),
      (try_end),
  ]),
]
