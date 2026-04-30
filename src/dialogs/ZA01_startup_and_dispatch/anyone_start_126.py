DIALOGS = [
[anyone , "start", [(is_between, "$g_talk_troop", mayors_begin, mayors_end), (eq, "$g_talk_troop_met", 0),
                     (this_or_next|eq, "$players_kingdom", "$g_encountered_party_faction"),
                     (             eq, "$g_encountered_party_faction", "fac_player_supporters_faction"), ],
   "Good day, my lord.", "mayor_begin", []],
]
