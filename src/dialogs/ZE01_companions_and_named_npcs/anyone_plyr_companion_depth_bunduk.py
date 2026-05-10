DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc10"),
    (main_party_has_troop, "trp_npc10"),
    (eq, "$g_sod_bunduk_line_pending", 1),
    (troop_slot_eq, "trp_npc10", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Bunduk, bring me the line's grievance plainly.", "companion_depth_bunduk_line_pending",
  []],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc10"),
    (main_party_has_troop, "trp_npc10"),
  ],
  "Bunduk, how does the line see my command?", "companion_depth_bunduk",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc10"),
  ]],
]
