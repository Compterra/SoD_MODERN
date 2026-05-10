DIALOGS = [
[anyone|plyr, "serpent_host_world_route_talk", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 400),
  ], "Shadow the Black Khergit horde for me.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 400),
    (call_script, "script_sod_serpent_host_apply_player_action", sod_serpent_action_track_horde, 8),
    (display_message, "@Serpent riders split off to mark Black Khergit movement and warn the next rich road.", 0x66AA66),
    (assign, "$g_leave_encounter", 1),
  ]],
]
