SCRIPTS = [
("party_copy",
    [
      (assign, "$g_move_heroes", 1),
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (try_begin),
        (gt, ":target_party", 0),
        (party_is_active, ":target_party"),
        (gt, ":source_party", 0),
        (party_is_active, ":source_party"),
        (party_clear, ":target_party"),
        (call_script, "script_party_add_party", ":target_party", ":source_party"),
      (try_end),
  ]),
]
