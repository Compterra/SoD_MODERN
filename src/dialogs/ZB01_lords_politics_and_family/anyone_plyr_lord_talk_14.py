DIALOGS = [
[anyone|plyr, "lord_talk", [#(troop_slot_eq, "$g_talk_troop", slot_troop_is_prisoner, 0),
               (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),
                             (eq, "$players_oath_renounced_against_kingdom", "$g_talk_troop_faction"),
                             (str_store_faction_name, s4, "$g_talk_troop_faction"), ],
   "{s66}, I broke faith with {s4}. I would have that oath judged again.", "lord_ask_pardon_after_oath_renounced", []],
]
