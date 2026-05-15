DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc9"),
    (main_party_has_troop, "trp_npc9"),
    (eq, "$g_sod_alayen_standard_pending", 1),
    (eq, "$g_sod_alayen_standard_confronted", 1),
    (troop_slot_eq, "trp_npc9", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Alayen, what does the standard ask of us?", "companion_depth_alayen_standard_pending",
  []],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc9"),
    (main_party_has_troop, "trp_npc9"),
  ],
  "Alayen, does my command still honor it?", "companion_depth_alayen",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc9"),
  ]],
]
