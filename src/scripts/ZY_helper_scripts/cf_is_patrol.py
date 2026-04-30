SCRIPTS = [
("cf_is_patrol",
                      [
                        (store_script_param, ":cur_party", 1),
                        (assign, reg0, 0),
                        (store_faction_of_party, ":cur_faction", ":cur_party"),
                        (eq, ":cur_faction", "fac_player_faction"),
                        (neq, ":cur_party", "p_main_party"),
                        (assign, reg0, 1),
                      ]
                    ),
]
