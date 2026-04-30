DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_ally_thanks),
                    (troop_is_hero, "$g_talk_troop"),
                    (eq, "$g_talk_troop_met", 0),
                    (ge, "$g_talk_troop_relation", 17),
                    ],
   "I don't think we have met properly my friend. You just saved my life out there, and I still don't know your name...", "ally_thanks_meet", []],
]
