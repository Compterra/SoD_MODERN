DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc14"),
    (main_party_has_troop, "trp_npc14"),
    (eq, "$g_sod_lezalit_ief_discipline_pending", 1),
    (troop_slot_eq, "trp_npc14", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Lezalit, show me the captured Imperial drill.", "companion_depth_lezalit_drill_pending",
  []],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc14"),
    (main_party_has_troop, "trp_npc14"),
  ],
  "Lezalit, speak plainly. What do you see in my command?", "companion_depth_lezalit",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc14"),
  ]],
]
