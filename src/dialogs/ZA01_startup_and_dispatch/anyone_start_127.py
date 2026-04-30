DIALOGS = [
[anyone , "start", [(is_between, "$g_talk_troop", mayors_begin, mayors_end), (eq, "$g_talk_troop_met", 0),
                     (str_store_party_name, s9, "$current_town")],
   "Hello stranger, you seem to be new to {s9}. I am the guild master of the town.", "mayor_talk", []],
]
