DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc5"),
    (main_party_has_troop, "trp_npc5"),
    (eq, "$g_sod_baheshtur_saddle_pending", 1),
    (eq, "$g_sod_baheshtur_saddle_confronted", 1),
    (troop_slot_eq, "trp_npc5", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Baheshtur, speak for the beaten riders.", "companion_depth_baheshtur_saddle_pending",
  []],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc5"),
    (main_party_has_troop, "trp_npc5"),
  ],
  "Baheshtur, is this ride still freely chosen?", "companion_depth_baheshtur",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc5"),
  ]],
]
