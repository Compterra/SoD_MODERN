DIALOGS = [
[anyone|plyr, "jotnar_world_hearth_talk", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 300),
  ], "Take 300 denars for hearth stores and winter medicine.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 300),
    (call_script, "script_sod_jotnar_apply_player_support", 2),
    (display_message, "@The Jotnar accept your gift. Hearth pressure eases and the clan remembers.", 0x99CCFF),
    (assign, "$g_leave_encounter", 1),
  ]],
]
