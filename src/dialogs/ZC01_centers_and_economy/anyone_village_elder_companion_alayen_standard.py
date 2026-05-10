DIALOGS = [
[anyone, "village_elder_companion_alayen_standard",
  [],
  "They saw armed cloth, my {lord/lady}. That can mean a shield or a tax collector, mercy or memory. If your banner means protection, make one promise under it and keep that promise where children can see.",
  "village_elder_talk",
  [
    (assign, "$g_sod_alayen_standard_witnessed", 1),
    (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_progress, 50),
    (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_metadata, "$g_sod_alayen_standard_result_grade"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_help_village, 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc9"),
    (display_message, "@A village elder gives Alayen's standard oath a protected-people witness.", 0x99CCFF),
  ]],
]
