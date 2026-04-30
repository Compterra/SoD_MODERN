DIALOGS = [
[anyone|plyr, "lord_join_rebellion_suggest_3", [(troop_get_type, reg39, "$g_talk_troop"),
      ], "Self-interest -- {s45} will reward  {reg39?her:his} followers well.", "lord_join_rebellion_suggest_4",
   [
        (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_benefit),
        (val_add, "$player_made_benefit_claim", 1),



        (assign, "$current_argument", argument_benefit),
        (assign, "$current_argument_value", reg0),

    ]],
]
