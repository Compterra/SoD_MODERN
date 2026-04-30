DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_kill_local_merchant"),
                         (check_quest_failed, "qst_kill_local_merchant")],
   "Oh, it's you. Enlighten me, how exactly does one lose a simple fight to some poxy, lowborn merchant?"\
   "Truly, if I ever need my guardsmen to take a lesson in how to lay down and die, I'll be sure to come to you."\
   "Just leave me be, {playername}, I have things to do.", "close_window",
   [(call_script, "script_end_quest", "qst_kill_local_merchant"),
    (assign, "$g_leave_encounter", 1)]],
]
