SCRIPTS = [
("game_reset_player_party_name",
    [(call_script, "script_store_troop_name_fief", s5, "trp_player"),
      (party_set_name, "p_main_party", s5),
  ]),
]
