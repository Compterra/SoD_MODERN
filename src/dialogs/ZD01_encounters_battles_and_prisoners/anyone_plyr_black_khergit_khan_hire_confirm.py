DIALOGS = [
[anyone|plyr, "black_khergit_khan_hire_confirm", [
    (store_troop_gold, ":player_gold", "trp_player"),
    (ge, ":player_gold", "$g_sod_black_khergit_hire_cost"),
    (store_add, ":total_hired", "$g_sod_black_khergit_hire_horsemen", "$g_sod_black_khergit_hire_guards"),
    (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
    (ge, ":free_capacity", ":total_hired"),
  ], "Done. Send them to my line.", "close_window", [
    (call_script, "script_sod_black_khergits_buy_hire_offer"),
    (assign, "$g_leave_encounter", 1),
  ]],
]
