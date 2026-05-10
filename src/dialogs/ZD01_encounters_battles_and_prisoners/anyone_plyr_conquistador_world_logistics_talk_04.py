DIALOGS = [
[anyone|plyr, "conquistador_world_logistics_talk", [
   (store_troop_gold, ":player_gold", "trp_player"),
   (ge, ":player_gold", 450),
  ], "Put 450 denars into your expedition stores.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 450),
    (call_script, "script_sod_conquistador_apply_player_action", sod_conquistador_action_fund_supplies, 450),
    (display_message, "@Conquistador quartermasters enter your contribution into the expedition ledger.", 0xCCAA55),
    (assign, "$g_leave_encounter", 1),
  ]],
]
