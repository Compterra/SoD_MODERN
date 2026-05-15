DIALOGS = [
[party_tpl|pt_sh_spy, "start", [
    (check_quest_active, "qst_serpent_host_free_spy"),
    (neg|check_quest_concluded, "qst_serpent_host_free_spy"),
    (quest_slot_eq, "qst_serpent_host_free_spy", slot_quest_target_party, "$g_encountered_party"),
    (party_is_active, "$g_encountered_party"),
    ],
   "Thank you for getting me out, {sir/madam}. Can we reach Sukbathar now?", "sh_spy_encounter_1", []],
]
