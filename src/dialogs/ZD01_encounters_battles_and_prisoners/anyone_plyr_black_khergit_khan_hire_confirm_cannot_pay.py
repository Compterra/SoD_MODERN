DIALOGS = [
[anyone|plyr, "black_khergit_khan_hire_confirm", [
    (store_add, ":total_hired", "$g_sod_black_khergit_hire_horsemen", "$g_sod_black_khergit_hire_guards"),
    (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
    (lt, ":free_capacity", ":total_hired"),
  ], "I do not have room in my ranks for the whole string of riders.", "black_khergit_khan_hire_cannot_pay", []],
[anyone|plyr, "black_khergit_khan_hire_confirm", [
    (store_troop_gold, ":player_gold", "trp_player"),
    (lt, ":player_gold", "$g_sod_black_khergit_hire_cost"),
  ], "I do not have that silver with me.", "black_khergit_khan_hire_cannot_pay", []],
]
