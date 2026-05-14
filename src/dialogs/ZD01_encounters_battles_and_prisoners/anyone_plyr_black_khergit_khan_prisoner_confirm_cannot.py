DIALOGS = [
[anyone|plyr, "black_khergit_khan_prisoner_confirm", [
    (this_or_next|lt, "$g_sod_black_khergit_prisoner_buy_count", 1),
    (lt, "$g_sod_black_khergit_prisoner_buy_cost", 1),
  ], "There is no bargain here after all.", "black_khergit_khan_talk", []],
[anyone|plyr, "black_khergit_khan_prisoner_confirm", [
    (store_troop_gold, ":player_gold", "trp_player"),
    (lt, ":player_gold", "$g_sod_black_khergit_prisoner_buy_cost"),
  ], "I cannot pay that price today.", "black_khergit_khan_talk", []],
[anyone|plyr, "black_khergit_khan_prisoner_confirm", [
    (party_get_free_prisoners_capacity, ":free_capacity", "p_main_party"),
    (lt, ":free_capacity", "$g_sod_black_khergit_prisoner_buy_count"),
  ], "I do not have enough guards to hold them.", "black_khergit_khan_talk", []],
[anyone|plyr, "black_khergit_khan_prisoner_confirm", [
    (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
    (lt, ":free_capacity", 1),
  ], "I have guards for chains, but no room for any of them in my ranks.", "black_khergit_khan_talk", []],
]
