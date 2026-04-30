DIALOGS = [
[anyone, "gm_bring_back_runaway_slaves_failed_1b", [],
   "Hah, now you reveal your true colours, traitor! Your words match your actions all too well. I should never have trusted you.", "close_window",
   [(call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", -10),
    (call_script, "script_change_player_honor", 5),
    (call_script, "script_fail_quest", "qst_slavers_bring_back_runaway_slaves"),
    (call_script, "script_end_quest", "qst_slavers_bring_back_runaway_slaves"),
    (assign, "$g_leave_encounter", 1),
  (finish_mission),
    ]],
]
