DIALOGS = [
[anyone, "lord_companion_alayen_standard",
  [
    (try_begin),
      (eq, "$g_sod_alayen_standard_cause", 2),
      (str_store_string, s4, "@In a hall, a banner promises precedence, allies, and enemies who know where to aim"),
    (else_try),
      (str_store_string, s4, "@Among frightened villages, a banner promises either shelter or another armed appetite"),
    (try_end),
  ],
  "{s4}. Your young noble is right to ask. Cloth becomes honor only when men can predict what it will cost you.",
  "lord_talk",
  [
    (assign, "$g_sod_alayen_standard_witnessed", 1),
    (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_progress, 50),
    (quest_set_slot, "qst_companion_alayen_standard_self", slot_quest_sod_runtime_metadata, "$g_sod_alayen_standard_result_grade"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_honorable_peace, 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc9"),
    (display_message, "@A lord gives Alayen's standard oath a public witness.", 0x99CCFF),
  ]],
]
