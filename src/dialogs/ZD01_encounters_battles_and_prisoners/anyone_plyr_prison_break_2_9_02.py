DIALOGS = [
[anyone|plyr, "prison_break_2_9", [], "Sorry, but I won't risk my neck. This whole case just isn't worth that much.", "close_window",
   [(assign, "$prison_break", -1),
    (call_script, "script_fail_quest", "qst_slave_q2"),
    (call_script, "script_end_quest", "qst_slave_q2")]],
]
