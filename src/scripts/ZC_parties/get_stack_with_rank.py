SCRIPTS = [
("get_stack_with_rank",
    [
      (store_script_param_1, ":party"), #Party_id
      (store_script_param_2, ":rank"), #Rank
      (assign, reg(0), -1),
      (try_begin),
        (gt, ":party", 0),
        (party_is_active, ":party"),
        (ge, ":rank", 0),
        (party_get_num_companion_stacks, ":num_stacks", ":party"),
        (assign, ":num_total", 0),
        (try_for_range, ":i_stack", 0, ":num_stacks"),
          (eq, reg(0), -1), #continue only if we haven't found the result yet.
          (party_stack_get_troop_id,     ":stack_troop", ":party", ":i_stack"),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size,         ":stack_size", ":party", ":i_stack"),
          (party_stack_get_num_wounded,  ":num_wounded", ":party", ":i_stack"),
          (val_sub, ":stack_size", ":num_wounded"),
          (val_max, ":stack_size", 0),
          (val_add, ":num_total", ":stack_size"),
          (try_begin),
            (lt, ":rank", ":num_total"),
            (assign, reg(0), ":i_stack"),
          (try_end),
        (try_end),
      (try_end),
  ]),
]
