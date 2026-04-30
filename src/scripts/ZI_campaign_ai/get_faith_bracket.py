SCRIPTS = [
("get_faith_bracket",
                      [
                        (store_script_param, reg0, 1),
                        (val_clamp, reg0, -100, 101),
                        (val_add, reg0, 100), # normalize 0..200
                        (val_sub, reg0, 12),  # shift down by 1/2 of a range
                        (val_div, reg0, 25),  # 0..8
                      ]
                    ),
]
