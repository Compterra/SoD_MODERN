DIALOGS = [
[anyone, "start", [(eq, "$talk_context", tc_party_encounter),
                    (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
                    (lt, "$g_encountered_party_relation", 0),
                    (encountered_party_is_attacker),
                    (eq, "$g_talk_troop_met", 1),                    ],
   "{playername}!", "party_encounter_lord_hostile_attacker", [
                    ]],
]
