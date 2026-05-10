DIALOGS = [
[anyone|plyr, "town_dweller_talk",
  [
    (party_slot_eq, "$current_town", slot_party_type, spt_town),
    (main_party_has_troop, "trp_npc4"),
    (eq, "$g_sod_rolf_name_challenge_pending", 1),
    (eq, "$g_sod_rolf_name_challenge_focus_center", "$current_town"),
    (eq, "$g_sod_rolf_name_challenge_witnessed", 0),
    (eq, "$g_sod_rolf_name_challenge_confronted", 0),
    (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "You heard Rolf's name in the street. What are people saying?", "town_dweller_companion_rolf_name", []],
]
