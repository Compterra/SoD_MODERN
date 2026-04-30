SCRIPTS = [
("party_move_slot",
                      [
                        (store_script_param, ":party", 1),
                        (store_script_param, ":new_slot", 2),
                        (store_script_param, ":offset", 3),

                        (store_add, ":old_slot", ":new_slot",":offset"),
                        (party_get_slot, ":value", ":party", ":old_slot"),
                        (party_set_slot, ":party", ":new_slot", ":value"),
                      ]
                    ),
]
