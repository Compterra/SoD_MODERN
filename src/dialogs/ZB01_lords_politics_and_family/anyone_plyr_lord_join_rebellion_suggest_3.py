DIALOGS = [
[anyone|plyr, "lord_join_rebellion_suggest_3", [(troop_get_type, reg39, "$g_talk_troop"),
      ], "Legality -- {s45} has the better claim to the throne", "lord_join_rebellion_suggest_4",
   [
        (call_script, "script_rebellion_arguments", "$g_talk_troop", argument_claim),
        (val_add, reg0, "$sod_rebel_pressure_mod"),
        (val_add, "$player_made_legitimacy_claim", 1),


        (assign, "$current_argument", argument_claim),
        (assign, "$current_argument_value", reg0),

    ]],
]
