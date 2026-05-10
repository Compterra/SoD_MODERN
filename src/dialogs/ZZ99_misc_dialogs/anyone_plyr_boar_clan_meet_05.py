DIALOGS = [
[anyone|plyr, "boar_clan_meet", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 450),
  ], "Take 450 denars and move your toll mark elsewhere.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 450),
    (call_script, "script_sod_boar_clan_apply_player_action", sod_boar_action_hire_band, 450),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_safe_roadcraft, 2),
    (display_message, "@Boar Clan road captains take your silver and loosen their grip on this mark.", 0xCC8844),
    (assign, "$g_leave_encounter", 1),
  ]],
]
