DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", tavern_travelers_begin, tavern_travelers_end),
                     ],
   "Greetings, {playername}.", "tavern_traveler_talk", [(assign, "$traveler_land_asked", 0)]],
]
