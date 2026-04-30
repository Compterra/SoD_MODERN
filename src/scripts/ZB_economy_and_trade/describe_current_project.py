SCRIPTS = [
("describe_current_project",
                      [
                        (store_script_param, ":sreg", 1),
                        (store_script_param, ":center", 2),

                        (str_clear, ":sreg"),
                        (try_begin),
                          (party_get_slot, ":cur_improvement", ":center", slot_center_current_improvement),
                          (gt, ":cur_improvement", 0),
                          (call_script, "script_get_improvement_details", ":cur_improvement"),
                          (store_current_hours, ":cur_hours"),
                          (party_get_slot, ":finish_time", ":center", slot_center_improvement_end_hour),
                          (val_sub, ":finish_time", ":cur_hours"),
                          (store_div, reg8, ":finish_time", 24),
                          (val_max, reg8, 1),
                          (store_sub, reg9, reg8, 1),
						  (party_slot_eq, ":center", slot_town_lord, "trp_player"),
                          (str_store_string, ":sreg", "@You are currently building a {s0}, which should be completed in {reg8} day{reg9?s:}. "),
                          (assign, reg0, 1),
                        (else_try),
                          (assign, reg0, 0),
                        (try_end),
                      ]
                    ),
]
