DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc12"),
    (main_party_has_troop, "trp_npc12"),
    (eq, "$g_sod_jeremus_triage_pending", 1),
    (troop_slot_eq, "trp_npc12", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Jeremus, take me to the wounded. I will give the order myself.", "companion_depth_jeremus_triage_pending",
  []],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc12"),
    (main_party_has_troop, "trp_npc12"),
  ],
  "Jeremus, how are the wounded, and how are you?", "companion_depth_jeremus",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc12"),
  ]],
]
