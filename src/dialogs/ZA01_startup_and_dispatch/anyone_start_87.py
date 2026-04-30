DIALOGS = [
[anyone, "start", [(eq, "$talk_context", 0), (faction_slot_eq, "$g_encountered_party_faction", slot_faction_castle_guard_troop, "$g_talk_troop"), (eq, "$sneaked_into_town", 1),
                    (gt, "$g_time_since_last_talk", 0)],
   "Get out of my sight, beggar! You stink!", "castle_guard_sneaked_intro_1", []],
]
