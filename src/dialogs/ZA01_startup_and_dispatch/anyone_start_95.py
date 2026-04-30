DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (eq, "$g_talk_troop_met", 0),
                    (ge, "$g_talk_troop_relation", 0),
                    (call_script, "script_store_troop_name", s1, "$g_talk_troop"),
                    ],
   "Thanks for your help, stranger. We haven't met properly yet, have we? What is your name?", "ally_thanks_meet", []],
]
