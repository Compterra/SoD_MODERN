DIALOGS = [
[anyone, "lord_bring_back_runaway_serfs_failed_1a", [],
   "Hmph, that is hardly an excuse for failure, {playername}.\
 Now if you will excuse me, I need to recruit new men to work these fields before we all starve.", "lord_pretalk",
   [(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
    (call_script, "script_end_quest", "qst_bring_back_runaway_serfs")]],
]
