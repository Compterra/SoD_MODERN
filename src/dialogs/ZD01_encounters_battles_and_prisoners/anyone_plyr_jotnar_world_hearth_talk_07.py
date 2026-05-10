DIALOGS = [
[anyone|plyr, "jotnar_world_hearth_talk", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 250),
  ], "Take 250 denars and watch the slave road harder.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 250),
    (call_script, "script_sod_jotnar_apply_player_support", 3),
    (call_script, "script_sod_slavers_apply_player_action", sod_slaver_action_free_runaways, 3),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_jotnar_support, 2),
    (display_message, "@Jotnar scouts mark the slave road and move kin-shelters closer to the danger.", 0x99CCFF),
    (assign, "$g_leave_encounter", 1),
  ]],
]
