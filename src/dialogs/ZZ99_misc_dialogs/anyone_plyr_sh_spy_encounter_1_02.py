DIALOGS = [
[anyone|plyr, "sh_spy_encounter_1", [
    (check_quest_active, "qst_serpent_host_free_spy"),
    (neg|check_quest_concluded, "qst_serpent_host_free_spy"),
    (quest_slot_eq, "qst_serpent_host_free_spy", slot_quest_target_party, "$g_encountered_party"),
    (party_is_active, "$g_encountered_party"),
    ],
   "Stay hidden. I will come back for you.", "spy_wait", []],
]
