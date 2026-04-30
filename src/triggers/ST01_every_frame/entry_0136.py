SIMPLE_TRIGGERS = [
(0.1,
       [
         (eq, "$g_start_postbattle_forced_rest", 1),
		 (assign, "$g_start_postbattle_forced_rest", 0), #twan453
         
         (store_div, reg0, "$post_battle_forced_rest_time", 10),
         (display_log_message, "@Your party is exhausted after the fight and cannot move for {reg0} hours.", dark_gray),
         
         ]),
]
