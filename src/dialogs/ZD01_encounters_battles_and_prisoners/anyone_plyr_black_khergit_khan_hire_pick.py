DIALOGS = [
[anyone|plyr, "black_khergit_khan_hire_confirm", [
    (gt, "$g_sod_black_khergit_hire_cost", 0),
    (store_add, ":available", "$g_sod_black_khergit_hire_horsemen", "$g_sod_black_khergit_hire_guards"),
    (gt, ":available", 1),
    (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
    (gt, ":free_capacity", 0),
  ], "Line them up. I will choose the riders I can use.", "close_window", [
    (call_script, "script_sod_black_khergits_begin_individual_hire_offer"),
    (set_mercenary_source_party, "p_temp_party"),
    (change_screen_buy_mercenaries),
    (call_script, "script_sod_black_khergits_finish_individual_hire_offer"),
    (assign, "$g_leave_encounter", 1),
  ]],
]
