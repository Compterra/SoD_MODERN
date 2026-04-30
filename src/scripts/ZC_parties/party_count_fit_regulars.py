SCRIPTS = [
("party_count_fit_regulars",
    [
      (store_script_param_1, ":party"), #Party_id
      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (assign, reg0, 0),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop", ":party", ":i_stack"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size,         ":stack_size", ":party", ":i_stack"),
        (party_stack_get_num_wounded, ":num_wounded", ":party", ":i_stack"),
        (val_sub, ":stack_size", ":num_wounded"),
        (val_max, ":stack_size", 0),
        (val_add, reg0, ":stack_size"),
      (try_end),
  ]),
]
