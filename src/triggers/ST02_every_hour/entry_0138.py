SIMPLE_TRIGGERS = [
(1,
    [  (eq, "$g_is_in_forced_rest", 0),
       (val_sub, "$post_battle_forced_rest_time", 4),
       (val_max, "$post_battle_forced_rest_time", 0),
       ]),
]
