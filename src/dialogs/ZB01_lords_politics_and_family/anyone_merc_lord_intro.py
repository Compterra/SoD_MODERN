DIALOGS = [
[anyone, "merc_lord_intro", [
   (assign, ":string", "$g_talk_troop"),
   (val_sub, ":string", "trp_black_army_leader_1"),
   (val_add, ":string", "str_sod_merc_commander_1_intro"),
   (str_store_string, s5, ":string"),
   ],
   "{s5}", "merc_lord_ask_name", [],],
]
