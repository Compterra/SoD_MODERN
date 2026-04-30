DIALOGS = [
[anyone, "start", [(eq, "$talk_context", 0),
                    (is_between, "$g_talk_troop", regular_troops_begin, regular_troops_end),
                    (is_between, "$g_encountered_party_faction", kingdoms_begin, kingdoms_end),
                    (eq, "$players_kingdom", "$g_encountered_party_faction"),
                    (troop_slot_ge, "trp_player", slot_troop_renown, 100),
                    (str_store_party_name, s10, "$current_town"),
                     ], "Good day, {sir/madam}. It's nice having you here in {s10}.", "close_window", []],
]
