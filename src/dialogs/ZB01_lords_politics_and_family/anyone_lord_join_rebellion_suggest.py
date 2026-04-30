DIALOGS = [
[anyone, "lord_join_rebellion_suggest", [
                    (eq, "$talk_context", tc_party_encounter),
                    (encountered_party_is_attacker),
                    (lt, "$g_talk_troop_relation", -5),
      ], "I have no time to bandy words with the likes of you. Now defend yourself!",
   "party_encounter_lord_hostile_attacker_2",
   [
        (troop_set_slot, "$g_talk_troop", slot_troop_discussed_rebellion, 1),
    ]],
]
