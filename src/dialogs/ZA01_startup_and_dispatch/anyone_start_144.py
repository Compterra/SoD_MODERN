DIALOGS = [
[anyone, "start", [(eq, "$talk_context", 0),
                    (is_between, "$g_talk_troop", walkers_begin, walkers_end),
                     ], "Good day, {sir/madam}.", "town_dweller_talk", [(assign, "$welfare_inquired", 0), (assign, "$rumors_inquired", 0), (assign, "$info_inquired", 0)]],
]
