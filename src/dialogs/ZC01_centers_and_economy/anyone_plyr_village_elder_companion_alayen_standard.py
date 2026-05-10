DIALOGS = [
[anyone|plyr, "village_elder_talk",
  [
    (main_party_has_troop, "trp_npc9"),
    (eq, "$g_sod_alayen_standard_pending", 1),
    (eq, "$g_sod_alayen_standard_cause", 1),
    (eq, "$g_sod_alayen_standard_witnessed", 0),
    (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "My standard was raised over people needing protection. What did they see?", "village_elder_companion_alayen_standard", []],
]
