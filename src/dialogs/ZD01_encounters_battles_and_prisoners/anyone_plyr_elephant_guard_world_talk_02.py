DIALOGS = [
[anyone|plyr, "elephant_guard_world_talk", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 300),
  ], "Take 300 denars for grain, medicine, and road offerings.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 300),
    (call_script, "script_sod_elephant_guard_apply_player_support", 2),
    (display_message, "@The Elephant Guard accepts your offering. Their shrine stores and regard for you improve.", 0x8B4513),
    (assign, "$g_leave_encounter", 1),
  ]],
]
