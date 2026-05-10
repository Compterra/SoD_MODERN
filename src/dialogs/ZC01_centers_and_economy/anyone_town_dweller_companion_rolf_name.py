DIALOGS = [
[anyone, "town_dweller_companion_rolf_name",
  [],
  "Some cheer him because a tall tale warms a tavern. Some laugh because a name polished too hard shows the scratches. If he wants the town to remember him, let him do something useful where we can see it.",
  "town_dweller_talk",
  [
    (assign, "$g_sod_rolf_name_challenge_witnessed", 1),
    (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_progress, 50),
    (quest_set_slot, "qst_companion_rolf_name_worth_wearing", slot_quest_sod_runtime_metadata, "$g_sod_rolf_name_challenge_result_grade"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_tournament_glory, 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc4"),
    (display_message, "@A town witness turns Rolf's name challenge into a public matter.", 0x99CCFF),
  ]],
]
