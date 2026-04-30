DIALOGS = [
[anyone|plyr, "lord_talk", [
                            (faction_slot_eq, "$g_talk_troop_faction", slot_faction_leader, "$g_talk_troop"),
                            (troop_slot_eq, "$g_talk_troop", slot_troop_discussed_rebellion, 0),
                            (assign, ":pretender", 0),
                            (try_for_range, ":possible_pretender", pretenders_begin, pretenders_end),
                                (troop_slot_eq, ":possible_pretender", slot_troop_original_faction, "$g_talk_troop_faction"),
                                (assign, ":pretender", ":possible_pretender"),
                            (try_end),
                            (troop_slot_ge, ":pretender", slot_troop_met, 1),
                            (call_script, "script_store_troop_name", s45, ":pretender"),
                            (troop_get_type, reg3, ":pretender"),
                             ],
   "I have met in my travels one who calls {reg3?herself:himself} {s45}...", "liege_defends_claim_1", [
       ]],
]
