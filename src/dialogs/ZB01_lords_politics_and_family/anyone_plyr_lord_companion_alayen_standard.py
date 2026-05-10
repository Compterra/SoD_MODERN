DIALOGS = [
[anyone|plyr, "lord_talk",
  [
    (main_party_has_troop, "trp_npc9"),
    (eq, "$g_sod_alayen_standard_pending", 1),
    (eq, "$g_sod_alayen_standard_witnessed", 0),
    (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "You have seen my standard in public. What does it promise to the realm?", "lord_companion_alayen_standard", []],
]
