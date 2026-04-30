SCRIPTS = [
("get_item_cost_with_imod",
                    [
                      (store_script_param, ":item", 1),
                      (store_script_param, ":imod", 2),

                      (store_item_value, ":cost", ":item"),
                      (item_get_slot, ":multiplier", ":imod", slot_item_imod_cost),
                      (val_mul, ":cost", ":multiplier"),
                      (store_div, reg0, ":cost", 100),
                    ]
                  ),
]
