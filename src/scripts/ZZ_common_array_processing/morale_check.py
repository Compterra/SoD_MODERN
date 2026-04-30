SCRIPTS = [
("morale_check",
                      [
					  				  
                        (try_begin),
                          (lt, "$allies_coh", 500), #SoD let's change it to 500, with new higher values it's still quite low
                          (store_random_in_range, ":routed", 1, 101),
                          (assign, ":chance_ply", 101), #SoD let's change it to 90, with new higher values it's still quite low
						  (assign, ":allymod", "$allies_coh"),
						  (val_div, ":allymod", 5),
						  (val_sub, ":chance_ply", ":allymod"),
                        #  (val_sub, ":chance_ply", "$allies_coh"),
						#SoD end 
                          (try_begin),
                            (le, ":routed", ":chance_ply"),
                            (display_message, "@Morale of your troops wavers!", red),
                            (call_script, "script_flee_allies"),
                          (try_end),
                        (try_end),

                        (try_begin),
                          (lt, "$enemies_coh", 500), #SoD let's change it to 500, with new higher values it's still quite low
                          (store_random_in_range, ":routed", 1, 101),
                          (assign, ":chance_ply", 101), #SoD
						  (assign, ":enemymod", "$enemies_coh"),
						  (val_div, ":enemymod", 5),
						  (val_sub, ":chance_ply", ":enemymod"),
                        #SoD  (val_sub, ":chance_ply", "$enemies_coh"),
                          (try_begin),
                            (le, ":routed", ":chance_ply"),
                            (display_message, "@Morale of your enemies wavers!", green),
                            (call_script, "script_flee_enemies"),
                          (try_end),
                        (try_end),
                      ]
                    ),
]
