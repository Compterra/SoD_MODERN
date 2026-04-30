SCRIPTS = [
("clear_party_group",
    [
      (store_script_param_1, ":root_party"),
      (party_clear, ":root_party"),
      (party_get_num_attached_parties, ":num_attached_parties", ":root_party"),
      (try_for_range, ":attached_party_rank", 0, ":num_attached_parties"),
        (party_get_attached_party_with_rank, ":attached_party", ":root_party", ":attached_party_rank"),
        (call_script, "script_clear_party_group", ":attached_party"),
      (try_end),
  ]),
]
