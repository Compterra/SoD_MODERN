DIALOGS = [
[anyone|plyr, "elephant_guard_world_talk", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 350),
  ], "Take 350 denars and hunt the slave-road omens.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 350),
    (call_script, "script_sod_elephant_guard_apply_player_support", 3),
    (call_script, "script_sod_slavers_apply_player_action", sod_slaver_action_hostile, 2),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_elephant_guard_support, 2),
    (display_message, "@Elephant Guard wardens turn shrine-road scouts toward Slaver traffic.", 0x8B4513),
    (assign, "$g_leave_encounter", 1),
  ]],
]
