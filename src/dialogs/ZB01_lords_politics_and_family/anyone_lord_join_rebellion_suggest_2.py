DIALOGS = [
[anyone, "lord_join_rebellion_suggest_2", [
            (neq, "$prior_argument_value", 0),
      ], "{s47}", "lord_join_rebellion_suggest_2",
   [

           (try_begin),
                (gt, "$prior_argument_value", 10),
                (str_store_string, s47, "str_rebellion_prior_argument_very_favorable"),
                (str_store_string, s49, "str_but_comma_3"),
           (else_try),
                (gt, "$prior_argument_value", 0),
                (str_store_string, s47, "str_rebellion_prior_argument_favorable"),
                (str_store_string, s49, "str_but_comma_3"),
           (else_try),
                (is_between, "$prior_argument_value", -10, 0),
                (str_store_string, s47, "str_rebellion_prior_argument_unfavorable"),
                (str_store_string, s49, "str_and_comma_3"),
           (else_try),
                (lt, "$prior_argument_value", -10),
                (str_store_string, s47, "str_rebellion_prior_argument_very_unfavorable"),
                (str_store_string, s49, "str_and_comma_3"),
           (try_end),

            (val_add, "$rebellion_chance", "$prior_argument_value"),

            (assign, reg6, "$prior_argument_value", debug_color), #diagnostic only
            (assign, "$prior_argument_value", 0),

            (assign, reg7, "$rebellion_chance", debug_color), #diagnostic only
            (display_message, "@Prior argument effect: {reg6}, rebellion chance: {reg7}", debug_color), #diagnostic only

    ]],
]
