SCRIPTS = [
("get_nonempty_party_in_group",
    [
      (store_script_param_1, ":party_no"),
      (party_get_num_companion_stacks, ":num_companion_stacks", ":party_no"),
      (try_begin),
        (gt, ":num_companion_stacks", 0),
        (assign, reg0, ":party_no"),
      (else_try),
        (assign, reg0, -1),

        (party_get_num_attached_parties, ":num_attached_parties", ":party_no"),
        (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
          (lt, reg0, 0),
          (party_get_attached_party_with_rank, ":attached_party", ":party_no", ":attached_party_rank"),
          (call_script, "script_get_nonempty_party_in_group", ":attached_party"),
        (try_end),
      (try_end),
  ]),
]
