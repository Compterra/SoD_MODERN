DIALOGS = [
[anyone, "start", [(eq, "$talk_context", 0),
                    (is_between, "$g_talk_troop", regular_troops_begin, regular_troops_end),
                    (is_between, "$g_encountered_party_faction", kingdoms_begin, kingdoms_end),
                     ], "Mind your manners within the walls and we'll have no trouble.", "close_window", []],
]
