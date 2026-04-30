DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_party_encounter),
                    (eq, "$g_encountered_party_type", spt_kingdom_caravan),
                    (lt, "$g_encountered_party_relation", 0),
                    (faction_get_slot, ":faction_leader", "$g_encountered_party_faction", slot_faction_leader),
                    (call_script, "script_store_troop_name", s9, ":faction_leader"),
                    ],
   "Be warned, knave! This caravan is under the protection of {s9}.\
 Step out of our way or you will face his fury!", "merchant_talk", []],
]
