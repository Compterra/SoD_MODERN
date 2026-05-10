DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc4"),
    (main_party_has_troop, "trp_npc4"),
    (eq, "$g_sod_rolf_name_challenge_pending", 1),
    (eq, "$g_sod_rolf_name_challenge_confronted", 1),
    (troop_slot_eq, "trp_npc4", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Rolf, answer the question about your name here, not from a pose.", "companion_depth_rolf_name_pending",
  []],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc4"),
    (main_party_has_troop, "trp_npc4"),
  ],
  "Rolf, does the company still suit your name?", "companion_depth_rolf",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc4"),
  ]],
]
