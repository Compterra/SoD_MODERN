SCRIPTS = [
("stay_captive_for_hours",
        [(store_script_param, ":num_hours", 1),
          (store_current_hours, ":cur_hours"),
          (val_add, ":cur_hours", ":num_hours"),
          (val_max, "$g_check_autos_at_hour", ":cur_hours"),
          (val_add, ":num_hours", 1),
			  (try_begin),  #twan453
			  (eq, "$g_is_in_forced_rest", 1),
			  (rest_for_hours, 0,0,0),
			  (try_end),
		  (assign, "$g_is_in_forced_rest", 0), 
		  (assign, "$post_battle_forced_rest_time", 0),
		  (assign, "$g_start_postbattle_forced_rest", 0), #twan453
          (rest_for_hours, ":num_hours", 0, 0),
      ]),
]
