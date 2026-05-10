DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", village_elders_begin, village_elders_end), (eq, "$g_talk_troop_met", 0),
                    (str_store_party_name, s9, "$current_town"),
                    (party_slot_eq, "$current_town", slot_town_lord, "trp_player")],
   "Welcome to {s9}, my {lord/lady}. Your banner is new over our fields, so the people are listening for what kind of rule follows it. I am the elder, and I will speak for them as honestly as I can.", "village_elder_talk", []],
]
