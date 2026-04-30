SCRIPTS = [
("describe_center_health",
                      [
                        (store_script_param, ":sreg", 1),
                        (store_script_param, ":center_health", 2),

                        (call_script, "script_get_health_bracket", ":center_health"),
                        (val_add, reg0, "str_describe_health_abysmal"),
                        (str_store_string, ":sreg", reg0),
                      ]
                    ),
]
