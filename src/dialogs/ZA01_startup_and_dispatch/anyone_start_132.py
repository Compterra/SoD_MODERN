DIALOGS = [
[anyone , "start", [(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
                     (party_slot_eq, "$current_town", slot_town_lord, "trp_player")],
   "{My lord/My lady}, you honour our humble village with your presence.", "village_elder_talk", []],
]
