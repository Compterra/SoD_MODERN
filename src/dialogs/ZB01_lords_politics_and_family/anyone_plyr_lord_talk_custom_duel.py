DIALOGS = [
[anyone|plyr, "lord_talk",
  [
    (call_script, "script_cf_sod_valid_lord_duel_target", "$g_talk_troop"),
  ],
  "I would challenge you to a formal duel.", "close_window",
  [
    (assign, "$g_sod_custom_duel_target", "$g_talk_troop"),
    (assign, "$g_sod_custom_duel_result", 0),
    (assign, "$g_leave_encounter", 1),
    (jump_to_menu, "mnu_duel_menu"),
    (finish_mission),
  ]],
]
