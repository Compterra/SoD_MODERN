DIALOGS = [
[anyone|plyr, "lord_join_rebellion_suggest_3", [
      ], "None of the usual reasons. My thinking is a little different.", "lord_join_rebellion_suggest_4",
   [
        (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_none),

        (assign, "$current_argument", argument_none),
        (assign, "$current_argument_value", 0),

    ]],
]
