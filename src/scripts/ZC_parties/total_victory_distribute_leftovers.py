SCRIPTS = [
("total_victory_distribute_leftovers",
    [
      # After the capture/loot screens, redistribute anything still sitting in
      # p_temp_party back into the allied or reinforcement group.
      (try_begin),
        (gt, "$g_ally_party", 0),
        (distribute_party_among_party_group, "p_temp_party", "$g_ally_party"),
        (call_script, "script_cf_fix_party_size", "$g_ally_party", 0),
      (else_try),
        (party_get_num_attached_parties, ":num_quick_attachments", "p_main_party"),
        (gt, ":num_quick_attachments", 0),
        (party_get_attached_party_with_rank, ":helper_party", "p_main_party", 0),
        (distribute_party_among_party_group, "p_temp_party", ":helper_party"),
        (call_script, "script_cf_fix_party_size", ":helper_party", 0),
      (try_end),
  ]),
]
