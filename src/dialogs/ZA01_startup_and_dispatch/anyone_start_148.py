DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_court_talk),
                    (is_between, "$g_talk_troop", regular_troops_begin, regular_troops_end),
                    (is_between, "$g_encountered_party_faction", kingdoms_begin, kingdoms_end),
                    (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
                     ], "Your orders, {my lord/my lady}?", "hall_guard_talk", []],
]
