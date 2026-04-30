DIALOGS = [
[anyone, "lord_ask_enter_service", [(gt, "$players_kingdom", 0),
                                     (neq, "$players_kingdom", "$g_talk_troop_faction"),
                                     (faction_get_slot, ":players_lord", "$players_kingdom", slot_faction_leader),
                                     (neq, ":players_lord", "trp_player"),
                                     (call_script, "script_store_troop_name", s5, ":players_lord"),
                                     ], "You are already oath-bound to serve {s5}, are you not?", "lord_give_oath_under_oath_already", []],
]
