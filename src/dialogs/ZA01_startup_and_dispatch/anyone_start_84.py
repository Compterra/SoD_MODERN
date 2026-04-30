DIALOGS = [
[anyone, "start", [(eq, "$talk_context", 0), (faction_slot_eq, "$g_encountered_party_faction", slot_faction_prison_guard_troop, "$g_talk_troop"),
                    (this_or_next|eq, "$g_encountered_party_faction", "fac_player_supporters_faction"),
                    (             party_slot_eq, "$g_encountered_party", slot_town_lord, "trp_player")
                    ],
   "Good day, my {lord/lady}. Will you be visiting the prison?", "prison_guard_players", []],
]
