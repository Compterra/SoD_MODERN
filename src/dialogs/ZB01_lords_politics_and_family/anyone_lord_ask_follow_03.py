DIALOGS = [
[anyone, "lord_ask_follow", [(lt, "$g_talk_troop_relation", 25)],
   "{s43}", "close_window",
   [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_lord_follow_refusal_default"),
       (assign, "$g_leave_encounter", 1)]],
]
