DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_court_talk),
                    (is_between, "$g_talk_troop", regular_troops_begin, regular_troops_end),
                    (is_between, "$g_encountered_party_faction", kingdoms_begin, kingdoms_end),
                     ], "We are not supposed to talk while on guard, {sir/madam}.", "close_window", []],
]
