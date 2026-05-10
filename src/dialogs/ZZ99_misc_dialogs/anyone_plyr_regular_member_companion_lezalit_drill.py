DIALOGS = [
[anyone|plyr, "regular_member_talk",
  [
    (main_party_has_troop, "trp_npc14"),
    (eq, "$g_sod_lezalit_ief_discipline_pending", 1),
    (eq, "$g_sod_lezalit_ief_discipline_witnessed", 0),
    (eq, "$g_sod_lezalit_ief_discipline_confronted", 0),
    (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Lezalit has captured Imperial drill notes. How does that lesson sound from the line?", "regular_member_companion_lezalit_drill", []],
]
