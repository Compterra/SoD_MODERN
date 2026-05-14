DIALOGS = [
[anyone|plyr, "black_khergit_khan_prisoner_confirm", [
    (store_troop_gold, ":player_gold", "trp_player"),
    (gt, ":player_gold", 0),
    (party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
    (gt, ":free_capacity", 0),
    (gt, "$g_sod_black_khergit_prisoner_buy_count", 0),
  ], "Bring them forward one by one. Those who will take wages can join my ranks.", "black_khergit_khan_talk", [
    (call_script, "script_sod_black_khergits_begin_individual_prisoner_recruit_offer"),
    (set_mercenary_source_party, "p_temp_party"),
    (change_screen_buy_mercenaries),
    (call_script, "script_sod_black_khergits_finish_individual_prisoner_recruit_offer"),
  ]],
]
