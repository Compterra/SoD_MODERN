SCRIPTS = [
("game_reset_player_party_name",
    [
      (try_begin),
        (eq, "$g_sod_player_world_ready", 1),
        (main_party_has_troop, "trp_player"),
        (call_script, "script_store_troop_name_fief", s5, "trp_player"),
        (party_set_name, "p_main_party", s5),
      (try_end),
  ]),
]
