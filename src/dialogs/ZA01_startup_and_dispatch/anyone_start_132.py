DIALOGS = [
[anyone , "start", [(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
                     (party_slot_eq, "$current_town", slot_town_lord, "trp_player")],
   "{My lord/My lady}, the village is yours to command, but the fields still answer to rain, seed, and fear. Tell me what you require.", "village_elder_talk", []],
]
