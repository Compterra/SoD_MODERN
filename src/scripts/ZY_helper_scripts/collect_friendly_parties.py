SCRIPTS = [
("collect_friendly_parties",
    [
      (party_collect_attachments_to_party, "p_main_party", "p_collective_friends"),
      (try_begin),
        (gt, "$g_ally_party", 0),
        (party_collect_attachments_to_party, "$g_ally_party", "p_temp_party"),
        (assign, "$g_move_heroes", 1),
        (call_script, "script_party_add_party", "p_collective_friends", "p_temp_party"),
      (try_end),
  ]),
]
