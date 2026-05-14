SIMPLE_TRIGGERS = [
(0,
   [
      (map_free),
      (this_or_next|neq, "$g_sod_battle_commander_troop", "trp_player"),
      (eq, "$g_sod_battle_commander_active", 1),
      (call_script, "script_sod_battle_commander_reset"),
    ]),
]
