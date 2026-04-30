DIALOGS = [
[anyone|plyr, "lord_join_rebellion_suggest_3", [(troop_get_type, reg39, "$g_talk_troop"),
      ], "Justice -- {s45} will treat {reg39?her:his} subjects better than {s46}", "lord_join_rebellion_suggest_4",
   [
        (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_ruler),
        (val_add, "$player_made_ruler_claim", 1),


        (assign, "$current_argument", argument_ruler),
        (assign, "$current_argument_value", reg0),
    ]],
]
