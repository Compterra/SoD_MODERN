SCRIPTS = [
("get_item_difficulty_with_imod",
                    [
                      (store_script_param, ":item", 1),
                      (store_script_param, ":imod", 2),

                      (item_get_slot, ":base", ":item", slot_item_difficulty),
                      (try_begin),
                        (neq, ":base", 0),
                        (item_get_slot, ":adj", ":imod", slot_item_imod_require),
                        (store_add, reg0, ":base", ":adj"),
                      (else_try),
                        (assign, reg0, ":base"),
                      (try_end),
                    ]
                  ),
]
