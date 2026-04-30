DIALOGS = [
[anyone|plyr, "lord_join_rebellion_suggest_3", [
      ], "There is more than one reason. I will let you make up your own mind.", "lord_join_rebellion_suggest_4",
   [
        (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_none),

        (assign, "$current_argument", argument_none),
        (assign, "$current_argument_value", 0),

    ]],
]
