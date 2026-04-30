DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", village_elders_begin, village_elders_end), (eq, "$g_talk_troop_met", 0),
                    (str_store_party_name, s9, "$current_town")],
   "Good day, {sir/madam}, and welcome to {s9}. I am the elder of this village.", "village_elder_talk", []],
]
