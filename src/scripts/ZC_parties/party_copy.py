SCRIPTS = [
("party_copy",
    [
      (assign, "$g_move_heroes", 1),
      (store_script_param_1, ":target_party"), #Target Party_id
      (store_script_param_2, ":source_party"), #Source Party_id
      (party_clear, ":target_party"),
      (call_script, "script_party_add_party", ":target_party", ":source_party"),
  ]),
]
