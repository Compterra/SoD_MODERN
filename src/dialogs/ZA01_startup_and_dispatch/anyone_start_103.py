DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_ally_thanks),
                    (ge, "$g_relation_boost", 5),
                    ],
   "Thank you for your help {sir/madam}. Things didn't look very well for us but then you came up and everything changed.", "close_window", []],
]
