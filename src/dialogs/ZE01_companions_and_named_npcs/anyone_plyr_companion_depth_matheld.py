DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc8"),
    (main_party_has_troop, "trp_npc8"),
    (eq, "$g_sod_matheld_no_backward_step_pending", 1),
    (eq, "$g_sod_matheld_no_backward_step_confronted", 1),
    (troop_slot_eq, "trp_npc8", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Matheld, tell me what the line learned in that fight.", "companion_depth_matheld_step_pending",
  []],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc8"),
    (main_party_has_troop, "trp_npc8"),
  ],
  "Matheld, do you still trust my courage?", "companion_depth_matheld",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc8"),
  ]],
]
