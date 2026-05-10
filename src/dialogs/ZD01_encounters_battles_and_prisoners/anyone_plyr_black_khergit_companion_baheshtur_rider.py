DIALOGS = [
[anyone|plyr, "black_khergit_raider_talk",
  [
    (main_party_has_troop, "trp_npc5"),
    (eq, "$g_sod_baheshtur_saddle_pending", 1),
    (eq, "$g_sod_baheshtur_saddle_witnessed", 0),
    (eq, "$g_sod_baheshtur_saddle_confronted", 0),
    (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Baheshtur says beaten riders still choose their road. What would you choose?", "black_khergit_companion_baheshtur_rider", []],
]
