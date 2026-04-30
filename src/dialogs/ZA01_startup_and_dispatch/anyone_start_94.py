DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (eq, "$g_talk_troop_met", 0),
                    (ge, "$g_talk_troop_relation", 5),
                    ],
   "Your help was most welcome stranger. My name is {s1}. Can I learn yours?", "ally_thanks_meet", []],
]
