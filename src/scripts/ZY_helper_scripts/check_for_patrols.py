SCRIPTS = [
("check_for_patrols",
                      [
                        (assign, ":num", 0),
                        (try_for_parties, ":cur_party"),
                          (call_script, "script_cf_is_patrol", ":cur_party"),
                          (eq, reg0, 0),
                          (val_add, ":num", 1),
                        (try_end),
                        (assign, reg0, ":num"),
                      ]
                    ),
]
