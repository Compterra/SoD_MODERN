DIALOGS = [
[anyone|plyr, "lord_talk", [(eq, "$talk_context", tc_party_encounter),
                             (neq, "$g_encountered_party_faction", "$players_kingdom"),
                             (ge, "$g_encountered_party_relation", 0),
                                 ], "I'm here to deliver you my demands!", "lord_predemand", []],
]
