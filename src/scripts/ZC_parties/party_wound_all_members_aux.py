SCRIPTS = [
("party_wound_all_members_aux",
    [
      (store_script_param_1, ":party_no"),

      (try_begin),
        (gt, ":party_no", 0),
        (party_is_active, ":party_no"),
        (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
        (try_for_range, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
          (try_begin),
            (neg|troop_is_hero, ":stack_troop"),
            (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
            (party_wound_members, ":party_no", ":stack_troop", ":stack_size"),
          (else_try),
            (troop_set_health, ":stack_troop", 0),
          (try_end),
        (try_end),
        (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
        (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
          (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
          (call_script, "script_party_wound_all_members_aux", ":attached_party"),
        (try_end),
      (try_end),

  ]),
]
