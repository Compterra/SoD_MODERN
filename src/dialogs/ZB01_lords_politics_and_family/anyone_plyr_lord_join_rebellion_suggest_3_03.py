DIALOGS = [
[anyone|plyr, "lord_join_rebellion_suggest_3", [(troop_get_type, reg39, "$g_talk_troop"),
      ], "Expediency -- {s45} will win, and the sooner  {reg39?she:he} wins, the sooner this war will end.", "lord_join_rebellion_suggest_4",
   [
        (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_victory),
        (val_add, "$player_made_strength_claim", 1),


        (assign, "$current_argument", argument_victory),
        (assign, "$current_argument_value", reg0),

    ]],
]
