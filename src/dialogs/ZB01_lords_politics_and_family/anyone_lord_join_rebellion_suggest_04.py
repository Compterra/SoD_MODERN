DIALOGS = [
[anyone, "lord_join_rebellion_suggest",
   [
    (eq, "$g_rebellion_suggest_friends_stronger", 1),
    ], "{s43}", "lord_start",
   [
       (call_script, "script_lord_comment_to_s43", "$g_talk_troop", "str_talk_later_default"),
    ]],
]
