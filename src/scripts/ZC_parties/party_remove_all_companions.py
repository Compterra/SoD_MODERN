SCRIPTS = [
("party_remove_all_companions",
    [
      (store_script_param_1, ":party"), #Source Party_id
      (party_get_num_companion_stacks, ":num_companion_stacks", ":party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_companion_stacks"),
        (party_stack_get_troop_id,   ":stack_troop", ":party", ":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
        (party_stack_get_size,  ":stack_size", ":party", ":stack_no"),
        (party_remove_members, ":party", ":stack_troop",  ":stack_size"),
        (try_begin),
          (eq, ":party", "p_main_party"),
          (is_between, ":stack_troop", companions_begin, companions_end),
          (call_script, "script_sod_companion_cleanup_departed_companion", ":stack_troop"),
        (try_end),
      (try_end),
  ]),
]
