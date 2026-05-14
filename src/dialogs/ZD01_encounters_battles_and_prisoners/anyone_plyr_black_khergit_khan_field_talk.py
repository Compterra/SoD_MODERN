DIALOGS = [
[anyone|plyr, "black_khergit_khan_field_talk", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 750),
  ], "Take 750 denars and ride for richer roads.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 750),
    (call_script, "script_sod_black_khergits_apply_player_action", sod_black_khergit_action_bribe_target, 750),
    (display_message, "@Temujin accepts your bribe from horseback and sends scouts toward a new rich mark.", 0x222222),
    (assign, "$g_leave_encounter", 1),
  ]],
]
