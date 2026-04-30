DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_ally_thanks),
                    (ge, "$g_relation_boost", 10),
                    (party_get_num_companions, reg1, "$g_encountered_party"),
                    (val_sub, reg1, 1),
                    ],
   "Thank you for your help {sir/madam}. You saved {reg1?our lives:my life} out there.", "close_window", []],
]
