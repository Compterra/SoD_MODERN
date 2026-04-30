SCRIPTS = [
("check_friendly_kills",
    [(get_player_agent_own_troop_kill_count, ":count"),
      (try_begin),
        (neq, "$g_player_current_own_troop_kills", ":count"),
        (val_sub, ":count", "$g_player_current_own_troop_kills"),
        (val_add, "$g_player_current_own_troop_kills", ":count"),
        (val_mul, ":count", -1),
        (call_script, "script_change_player_party_morale", ":count"),
      (try_end),
  ]),
]
