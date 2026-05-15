DIALOGS = [
[anyone|plyr, "kidnapped_girl_encounter_1", [
    (check_quest_active, "qst_kidnapped_girl"),
    (neg|check_quest_concluded, "qst_kidnapped_girl"),
    (quest_slot_eq, "qst_kidnapped_girl", slot_quest_current_state, 2),
    (quest_slot_eq, "qst_kidnapped_girl", slot_quest_target_party, "$g_encountered_party"),
    (party_is_active, "$g_encountered_party"),
    ],
   "Yes. Stay close and I will get you home.", "kidnapped_girl_join", []],
]
