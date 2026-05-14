DIALOGS = [
[anyone, "start", [(eq, "$talk_context", 0), (ge, "$g_encountered_party_faction", 0), (faction_slot_eq, "$g_encountered_party_faction", slot_faction_castle_guard_troop, "$g_talk_troop")],
   "Hold there. Name your business before the gate captain starts guessing.", "castle_guard_intro_1", []],
]
