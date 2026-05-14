DIALOGS = [
[anyone, "start", [(eq, "$talk_context", 0), (ge, "$g_encountered_party_faction", 0), (faction_slot_eq, "$g_encountered_party_faction", slot_faction_prison_guard_troop, "$g_talk_troop")],
   "State your business. Prison stones hear enough lies without me inviting more of them.", "prison_guard_talk", []],
]
