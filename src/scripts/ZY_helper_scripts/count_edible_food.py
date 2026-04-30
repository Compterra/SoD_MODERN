SCRIPTS = [
("count_edible_food",
                      [
                        (assign, ":edible", 0),
                        (troop_get_inventory_capacity, ":inv_size", "trp_player"),
                        (try_for_range, ":i_slot", 0, ":inv_size"),
                          (troop_get_inventory_slot, ":cur_item", "trp_player", ":i_slot"),
                          (is_between, ":cur_item", food_begin, food_end),
                          (troop_get_inventory_slot_modifier, ":cur_modifier", "trp_player", ":i_slot"),
                          (neq, ":cur_modifier", imod_rotten),
                          (troop_inventory_slot_get_item_amount, ":amount", "trp_player", ":i_slot"),
                          (val_add, ":edible", ":amount"),
                        (try_end),
                        (assign, reg0, ":edible"),
                    ]),
]
