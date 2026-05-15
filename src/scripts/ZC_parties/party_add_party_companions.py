SCRIPTS = [
("party_add_party_companions",
    [
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (try_begin),
        (gt, ":target_party", 0),
        (party_is_active, ":target_party"),
        (gt, ":source_party", 0),
        (party_is_active, ":source_party"),
        (party_get_num_companion_stacks, ":num_stacks", ":source_party"),
        (try_for_range, ":stack_no", 0, ":num_stacks"),
          (party_stack_get_troop_id,     ":stack_troop", ":source_party", ":stack_no"),
          (this_or_next|neg|troop_is_hero, ":stack_troop"),
          (eq, "$g_move_heroes", 1),
          (party_stack_get_size,         ":stack_size", ":source_party", ":stack_no"),
          (party_add_members, ":target_party", ":stack_troop", ":stack_size"),
          (party_stack_get_num_wounded, ":num_wounded", ":source_party", ":stack_no"),
          (party_wound_members, ":target_party", ":stack_troop", ":num_wounded"),
        (try_end),
      (try_end),
  ]),
]
