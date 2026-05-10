SCRIPTS = [
("scan_for_best_item_of_type",
                      [
                        (store_script_param, ":pool", 1),
                        (store_script_param, ":item_type", 2),
                        (store_script_param, ":troop", 3),
                        (store_script_param, ":require_mount_compatible", 4),

                        # iterate through the list of items
                        (assign, ":best_slot", -1),
                        (assign, ":best_value", -1),
                        (troop_get_inventory_capacity, ":inv_cap", ":pool"),
                        (try_for_range, ":i_inventory", 0, ":inv_cap"),
                          (troop_get_inventory_slot, ":item", ":pool", ":i_inventory"),
                          (ge, ":item", 0),
                          (call_script, "script_sod_auto_loot_item_is_protected", ":item"),
                          (eq, reg0, 0),
                          (item_get_type, ":this_item_type", ":item"),
                          (eq, ":this_item_type", ":item_type"), # it's one of the kind we're looking for
                          (troop_get_inventory_slot_modifier, ":imod", ":pool", ":i_inventory"),
                          (call_script, "script_troop_can_use_item", ":troop", ":item", ":imod"),
                          (eq, reg0, 1), # can use

                          # make sure that we're either allowed to use foot-soldier only items, or that this item can be used on horseback
                          (this_or_next|eq, ":require_mount_compatible", 0),
                          (item_slot_eq, ":item", slot_item_cant_use_on_horseback, 0),

                          # get item_score instead of price
                          (call_script, "script_get_item_score_with_imod", ":item", ":imod"),

                          # check if this one is the best one we've seen yet
                          (gt, reg0, ":best_value"),
                          (assign, ":best_slot", ":i_inventory"),
                          (assign, ":best_value", reg0),
                        (try_end),

                        # return the slot of the best one
                        (assign, reg0, ":best_slot"),
                      ]
                    ),
]
