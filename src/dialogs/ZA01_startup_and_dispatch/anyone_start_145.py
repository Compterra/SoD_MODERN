DIALOGS = [
[anyone, "start", [(eq, "$talk_context", 0),
                    (is_between, "$g_talk_troop", regular_troops_begin, regular_troops_end),
                    (party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
                     ], "Yes {sir/madam}?", "player_castle_guard_talk", []],
]
