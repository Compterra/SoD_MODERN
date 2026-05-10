DIALOGS = [
[anyone, "black_khergit_companion_baheshtur_rider",
  [
    (try_begin),
      (eq, "$g_sod_baheshtur_saddle_cause", 2),
      (str_store_string, s4, "@A broken camp leaves many saddles empty"),
    (else_try),
      (str_store_string, s4, "@A broken raid leaves a rider choosing between rope and road"),
    (try_end),
  ],
  "{s4}. If your lord gives a horse and calls it a chain, I spit. If he gives a road and lets my word stand, I may ride it.",
  "close_window",
  [
    (assign, "$g_sod_baheshtur_saddle_witnessed", 1),
    (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_progress, 50),
    (quest_set_slot, "qst_companion_baheshtur_unbroken_saddle", slot_quest_sod_runtime_metadata, "$g_sod_baheshtur_saddle_result_grade"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_safe_roadcraft, 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc5"),
    (display_message, "@A Black Khergit rider gives Baheshtur's saddle oath a living witness.", 0x99CCFF),
    (assign, "$g_leave_encounter", 1),
  ]],
]
