DIALOGS = [
[anyone, "lord_suggest_lift_siege", [],
   "As you wish, {playername}.", "close_window", [(call_script, "script_party_set_ai_state", "$g_talk_troop_party", spai_undefined),
                                           (party_leave_cur_battle, "$g_talk_troop_party"),
                                           (assign, "$g_leave_encounter", 1)]],
]
