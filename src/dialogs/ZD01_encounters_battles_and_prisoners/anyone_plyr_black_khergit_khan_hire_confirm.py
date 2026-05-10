DIALOGS = [
[anyone|plyr, "black_khergit_khan_hire_confirm", [
    (store_troop_gold, ":player_gold", "trp_player"),
    (ge, ":player_gold", "$g_sod_black_khergit_hire_cost"),
  ], "Done. Send them to my line.", "close_window", [
    (call_script, "script_sod_black_khergits_buy_hire_offer"),
    (assign, "$g_leave_encounter", 1),
  ]],
]
