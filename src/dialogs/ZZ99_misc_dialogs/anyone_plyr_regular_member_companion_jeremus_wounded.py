DIALOGS = [
[anyone|plyr, "regular_member_talk",
  [
    (main_party_has_troop, "trp_npc12"),
    (eq, "$g_sod_jeremus_triage_pending", 1),
    (eq, "$g_sod_jeremus_triage_witnessed", 0),
    (eq, "$g_sod_jeremus_triage_confronted", 0),
    (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Jeremus says the wounded are waiting on my order. What have you seen?", "regular_member_companion_jeremus_wounded", []],
]
