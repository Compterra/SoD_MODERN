DIALOGS = [
[anyone|plyr, "black_khergit_khan_prisoner_confirm", [
    (store_troop_gold, ":player_gold", "trp_player"),
    (ge, ":player_gold", "$g_sod_black_khergit_prisoner_buy_cost"),
    (party_get_free_prisoners_capacity, ":free_capacity", "p_main_party"),
    (ge, ":free_capacity", "$g_sod_black_khergit_prisoner_buy_count"),
  ], "Done. Cut them loose and put them under my guard.", "black_khergit_khan_talk", [
    (call_script, "script_sod_black_khergits_buy_prisoners"),
  ]],
]
