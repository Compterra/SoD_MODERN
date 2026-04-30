DIALOGS = [
[anyone, "lord_bring_back_runaway_serfs_failed_1b", [],
   "Hah, now you reveal your true colours, traitor! Your words match your actions all too well. I should never have trusted you.", "close_window",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -10),
    (quest_get_slot, ":home_village", "qst_bring_back_runaway_serfs", slot_quest_object_center),
    (call_script, "script_change_player_relation_with_center", ":home_village", 6),
    (call_script, "script_end_quest", "qst_bring_back_runaway_serfs"),
    (assign, "$g_leave_encounter", 1),
    ]],
]
