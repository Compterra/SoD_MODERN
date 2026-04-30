SCRIPTS = [
("describe_center_faith",
                      [
                        (store_script_param, ":sreg", 1),
                        (store_script_param, ":faith", 2),

                        (call_script, "script_get_faith_bracket", ":faith"),
                        (val_add, reg0, "str_describe_faith_violent"),
                        (str_store_string, ":sreg", reg0),
                      ]
                    ),
]
