SCRIPTS = [
("describe_item_with_imod",
                      [
                        (store_script_param, ":sreg", 1),
                        (store_script_param, ":item", 2),
                        (store_script_param, ":imod", 3),

                        (try_begin),
                          (eq, ":item", -1),
                          (str_store_string, ":sreg", "@nothing"),
                        (else_try),
                          (store_add, ":string_id", "str_imod_0", ":imod"),
                          (str_store_item_name, s60, ":item"),
                          (str_store_string, ":sreg", ":string_id"),
                        (try_end),
                      ]
                    ),
]
