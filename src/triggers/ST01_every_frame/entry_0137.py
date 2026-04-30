SIMPLE_TRIGGERS = [
(0.1,
      [ (eq, "$g_is_in_forced_rest", 1),
        (val_sub, "$post_battle_forced_rest_time", 1),

        (try_begin),
        (le, "$post_battle_forced_rest_time", 0),
        (assign, "$g_is_in_forced_rest", 0),
        (rest_for_hours, 0, 0, 0), # interrupt the rest
		(else_try),
		(eq, "$g_sod_deactivate_forced_rest", 1),   #twan453 allowed to deactivate forced rest when resting
		(assign, "$g_is_in_forced_rest", 0),
        (rest_for_hours, 0, 0, 0), # interrupt the rest
        (try_end),
      ]),
]
