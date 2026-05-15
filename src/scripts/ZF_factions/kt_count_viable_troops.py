SCRIPTS = [
( "kt_count_viable_troops",
   [
      # remember our params
      (store_script_param_1, ":party"),   # party id
      (store_script_param_2, ":exclude_leader"), # also a party id apparently

      # clear out our return
      (assign, reg0, 0),

      (try_begin),
      (gt, ":party", 0),
      (party_is_active, ":party"),

      # figure out which stack to start with and how many we have
      (party_get_num_companion_stacks, ":num_stacks", ":party"),
      (assign, ":first_stack", 0),
      (try_begin),
         (neq, ":exclude_leader", 0),
         (assign, ":first_stack", 1),
      (try_end),

      (try_for_range, ":i_stack", ":first_stack", ":num_stacks"),
         (party_stack_get_troop_id, ":stack_troop", ":party", ":i_stack"),
         (party_stack_get_size, ":stack_size",":party",":i_stack"),
         (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
         (val_sub, ":stack_size", ":num_wounded"),
         (try_begin),
            (gt, ":stack_size", 0),
            (try_begin),
               # if this stack is a hero, check health vs. the viable thresh.
               (troop_is_hero, ":stack_troop"),
               (neg|troop_is_wounded, ":stack_troop"),
               (val_add, reg0, 1),
            (else_try),
               # otherwise just add
               (val_add, reg0, ":stack_size"),
            (try_end),
         (try_end),
      (try_end),
      (try_end),

      # reg0 should have the battle-ready count
   ]),
]
