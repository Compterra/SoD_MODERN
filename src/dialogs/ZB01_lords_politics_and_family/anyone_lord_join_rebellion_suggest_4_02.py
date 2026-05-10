DIALOGS = [
[anyone, "lord_join_rebellion_suggest_4", [

      ], "Very well. {s51}{s52}{s53}{s54}{s55}", "lord_join_rebellion_suggest_5",
   [

        (try_for_range, ":clear", 51, 60),
            (str_clear, ":clear"),
        (try_end),

        (try_begin),
            (neq, "$current_argument", argument_none),
            (try_begin),
                (gt, "$current_argument_value", 0),
                (str_store_string, 51, "str_rebellion_argument_favorable"),
            (else_try),
                (eq, "$current_argument_value", 0),
                (str_store_string, 51, "str_rebellion_argument_neutral"),
            (else_try),
                (lt, "$current_argument_value", 0),
                (str_store_string, 51, "str_rebellion_argument_unfavorable"),
            (try_end),

            (val_add, "$rebellion_chance", "$current_argument_value"),

            (assign, reg6, "$current_argument_value"),
            (assign, reg7, "$rebellion_chance"),
            (try_begin),
              (eq, "$cheat_mode", 1),
              (display_message, "@Current argument effect: {reg6}, rebellion chance: {reg7}", debug_color),
            (try_end),

            (store_skill_level, ":persuasion_level", "skl_persuasion", "trp_player"),
            (val_mul, ":persuasion_level", 5),
            (store_random_in_range, ":persuasion_value", -10, ":persuasion_level"),


            (store_add, ":persuasion_plus_argument", ":persuasion_value", "$current_argument_value"),

            (str_store_string, 52, "str_and_comma_1"),

            (try_begin),
                (gt, ":persuasion_value", 10),
                (str_store_string, 53, "str_rebellion_persuasion_favorable"),
                (try_begin),
                    (lt, "$current_argument_value", 0),
                    (str_store_string, 52, "str_but_comma_1"),
                (try_end),
            (else_try),
                (lt, ":persuasion_plus_argument", 0),
                (lt, ":persuasion_value", 0),
                (str_store_string, 53, "str_rebellion_persuasion_unfavorable"),
                (try_begin),
                    (ge, "$current_argument_value", 0),
                    (str_store_string, 52, "str_but_comma_1"),
                (try_end),
            (else_try),
                (str_store_string, 53, "str_rebellion_persuasion_neutral"),
                (try_begin),
                    (lt, "$current_argument_value", 0),
                    (str_store_string, 52, "str_but_comma_1"),
                (try_end),
            (try_end),

            (val_add, "$rebellion_chance", ":persuasion_value"),

            (assign, reg6, ":persuasion_value"),
            (assign, reg7, "$rebellion_chance"),
            (try_begin),
              (eq, "$cheat_mode", 1),
              (display_message, "@Persuasion effect: {reg6}, rebellion chance: {reg7}", debug_color),
            (try_end),

            (str_store_string, 54, "str_and_comma_2"),
            (try_begin),
                (gt, ":persuasion_plus_argument", 0),
                (lt, "$g_talk_troop_relation", 5),
                (str_store_string, 54, "str_but_comma_2"),
            (else_try),
                (le, ":persuasion_plus_argument", 0),
                (ge, "$g_talk_troop_relation", 5),
                (str_store_string, 54, "str_but_comma_2"),
            (try_end),

        (try_end),

        (try_begin),
            (gt, "$g_talk_troop_relation", 20),
            (str_store_string, 55, "str_rebellion_relation_very_favorable"),
        (else_try),
            (gt, "$g_talk_troop_relation", 5),
            (str_store_string, 55, "str_rebellion_relation_favorable"),
        (else_try),
            (gt, "$g_talk_troop_relation", -5),
            (str_store_string, 55, "str_rebellion_relation_neutral"),
        (else_try),
            (str_store_string, 55, "str_rebellion_relation_unfavorable"),
        (try_end),

        (val_add, "$rebellion_chance", "$g_talk_troop_relation"),

        (assign, reg6, "$g_talk_troop_relation"),
        (assign, reg7, "$rebellion_chance"),
        (try_begin),
          (eq, "$cheat_mode", 1),
          (display_message, "@Personal relation effect: {reg6}, rebellion chance: {reg7}", debug_color),
        (try_end),


        (store_random_in_range, "$rebellion_check", 0, 100),

        (assign, reg6, "$rebellion_check"),
        (try_begin),
          (eq, "$cheat_mode", 1),
          (display_message, "@Rebellion check: {reg6}", debug_color),
        (try_end),


    ]],
]
