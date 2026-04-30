DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", village_elders_begin, village_elders_end), (eq, "$g_talk_troop_met", 0),
                    (str_store_party_name, s9, "$current_town"),
                    (party_slot_eq, "$current_town", slot_town_lord, "trp_player")],
   "Welcome to {s9}, my {lord/lady}. We were rejoiced by the news that you are the new {lord/lady} of our humble village.\
 I am the village elder and I will be honoured to serve you in any way I can.", "village_elder_talk", []],
]
