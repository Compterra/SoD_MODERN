DIALOGS = [
[anyone, "regular_member_companion_matheld_line",
  [
    (try_begin),
      (eq, "$g_sod_matheld_no_backward_step_cause", 2),
      (str_store_string, s4, "@we held, but too many men learned that courage means standing until someone else counts the bodies"),
    (else_try),
      (str_store_string, s4, "@we gave ground, and the sound of it stayed in the boots longer than the horn did"),
    (try_end),
  ],
  "What I saw? {s4}. Matheld is right to ask what lesson you want the next line to carry. Put us in a shield-line test where men can feel the difference.",
  "regular_member_talk",
  [
    (assign, "$g_sod_matheld_no_backward_step_witnessed", 1),
    (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_progress, 50),
    (quest_set_slot, "qst_companion_matheld_no_backward_step", slot_quest_sod_runtime_metadata, "$g_sod_matheld_no_backward_step_result_grade"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_hard_victory, 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc8"),
    (display_message, "@A ranker gives Matheld's shield challenge a post-battle witness. The line wants a test, not another speech.", 0x99CCFF),
  ]],
]
