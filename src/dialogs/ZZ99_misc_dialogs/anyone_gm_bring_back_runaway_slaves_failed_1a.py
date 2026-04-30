DIALOGS = [
[anyone, "gm_bring_back_runaway_slaves_failed_1a", [],
   "Hmph, that is hardly an excuse for failure, {playername}.\
 Now if you will excuse me, I need to catch some new slaves.", "lord_pretalk",
   [(call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", -1),
    (call_script, "script_fail_quest", "qst_slavers_bring_back_runaway_slaves"),
    (call_script, "script_end_quest", "qst_slavers_bring_back_runaway_slaves")]],
]
