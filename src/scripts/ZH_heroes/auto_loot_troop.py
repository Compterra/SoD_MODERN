SCRIPTS = [
("auto_loot_troop",
                      [
                        (store_script_param, ":troop", 1),
                        (store_script_param, ":pool", 2),
                        (store_script_param, ":require_mount_compatible", 3),

                        (troop_get_slot, ":upg_armor", ":troop", slot_troop_upgrade_armor),
                        (troop_get_slot, ":upg_horses", ":troop", slot_troop_upgrade_horse),

                        # dump whatever rubbish is in the troop's main inventory
                        (troop_get_inventory_capacity, ":inv_cap", ":troop"),
                        (try_for_range, ":i_inventory", first_inventory_slot, ":inv_cap"),
                          (troop_get_inventory_slot, ":item", ":troop", ":i_inventory"),
                          (ge, ":item", 0),
                          (troop_get_inventory_slot_modifier, ":imod", ":troop", ":i_inventory"),
                          (troop_add_item, ":pool", ":item", ":imod"), #put it back in the pool
                          (troop_set_inventory_slot, ":troop", ":i_inventory", -1), # delete it
                        (try_end),

                        # dispose of the troop's equipped items if necessary
                        (try_begin),
                          (troop_slot_ge, ":troop", slot_troop_upgrade_wpn_0, 1),
                          (troop_get_inventory_slot, ":item", ":troop", ek_item_0),
                          (ge, ":item", 0),
                          (troop_get_inventory_slot_modifier, ":imod", ":troop", ek_item_0),
                          (troop_set_inventory_slot, ":troop", ek_item_0, -1), #delete it
                          (troop_add_item, ":pool", ":item", ":imod"), # chuck it in the pool
                        (try_end),

                        (try_begin),
                          (troop_slot_ge, ":troop", slot_troop_upgrade_wpn_1, 1),
                          (troop_get_inventory_slot, ":item", ":troop", ek_item_1),
                          (ge, ":item", 0),
                          (troop_get_inventory_slot_modifier, ":imod", ":troop", ek_item_1),
                          (troop_set_inventory_slot, ":troop", ek_item_1, -1), #delete it
                          (troop_add_item, ":pool", ":item", ":imod"), # chuck it in the pool
                        (try_end),

                        (try_begin),
                          (troop_slot_ge, ":troop", slot_troop_upgrade_wpn_2, 1),
                          (troop_get_inventory_slot, ":item", ":troop", ek_item_2),
                          (ge, ":item", 0),
                          (troop_get_inventory_slot_modifier, ":imod", ":troop", ek_item_2),
                          (troop_set_inventory_slot, ":troop", ek_item_2, -1), #delete it
                          (troop_add_item, ":pool", ":item", ":imod"), # chuck it in the pool
                        (try_end),

                        (try_begin),
                          (troop_slot_ge, ":troop", slot_troop_upgrade_wpn_3, 1),
                          (troop_get_inventory_slot, ":item", ":troop", ek_item_3),
                          (ge, ":item", 0),
                          (troop_get_inventory_slot_modifier, ":imod", ":troop", ek_item_3),
                          (troop_set_inventory_slot, ":troop", ek_item_3, -1), #delete it
                          (troop_add_item, ":pool", ":item", ":imod"), # chuck it in the pool
                        (try_end),

                        (try_for_range, ":i_inventory", ek_head, ek_food),
                          (troop_get_inventory_slot, ":item", ":troop", ":i_inventory"),
                          (ge, ":item", 0),
                          (troop_get_inventory_slot_modifier, ":imod", ":troop", ":i_inventory"),
                          (try_begin),
                            (neq, ":upg_armor", 0), # we're uprgrading armors
                            (is_between, ":i_inventory", ek_head, ek_horse), # it's an armor slot
                            (troop_set_inventory_slot, ":troop", ":i_inventory", -1), #delete it
                            (troop_add_item, ":pool", ":item", ":imod"), # chuck it in the pool
                          (else_try),
                            (neq, ":upg_horses", 0), # we're uprgrading horses
                            (eq, ":i_inventory", ek_horse), # it's a horse slot
                            (troop_set_inventory_slot, ":troop", ":i_inventory", -1), #delete it
                            (troop_add_item, ":pool", ":item", ":imod"), # chuck it in the pool
                          (try_end),
                        (try_end),

                        # clear best matches
                        (assign, ":best_helmet_slot", -1),
                        (assign, ":best_helmet_val", 0),
                        (assign, ":best_body_slot", -1),
                        (assign, ":best_body_val", 0),
                        (assign, ":best_boots_slot", -1),
                        (assign, ":best_boots_val", 0),
                        (assign, ":best_gloves_slot", -1),
                        (assign, ":best_gloves_val", 0),
                        (assign, ":best_horse_slot", -1),
                        (assign, ":best_horse_val", 0),

                        # Now search through the pool for the best items
                        (troop_get_inventory_capacity, ":inv_cap", ":pool"),
                        (try_for_range, ":i_inventory", 0, ":inv_cap"),

                          # check if there is an item in this inventory slot
                          (troop_get_inventory_slot, ":item", ":pool", ":i_inventory"),
                          (ge, ":item", 0),

                          # check if this troop can use this item
                          (troop_get_inventory_slot_modifier, ":imod", ":pool", ":i_inventory"),
                          (call_script, "script_troop_can_use_item", ":troop", ":item", ":imod"),
                          (eq, reg0, 1), # can use

                          # Rubik - get item_score instead of price
                          (call_script, "script_get_item_score_with_imod", ":item", ":imod"),
                          (assign, ":score", reg0),

                          (item_get_type, ":item_type", ":item"),

                          (try_begin),
                            (eq, ":item_type", itp_type_horse), #it's a horse
                            (eq, ":upg_horses", 1), # we're uprgrading horses
                            (gt, ":score", ":best_horse_val"),
                            (assign, ":best_horse_slot", ":i_inventory"),
                            (assign, ":best_horse_val", ":score"),
                          (else_try),
                            (eq, ":item_type", itp_type_head_armor),
                            (eq, ":upg_armor", 1), # we're uprgrading armor
                            (gt, ":score", ":best_helmet_val"),
                            (assign, ":best_helmet_slot", ":i_inventory"),
                            (assign, ":best_helmet_val", ":score"),
                          (else_try),
                            (eq, ":item_type", itp_type_body_armor),
                            (eq, ":upg_armor", 1), # we're uprgrading armor
                            (gt, ":score", ":best_body_val"),
                            (assign, ":best_body_slot", ":i_inventory"),
                            (assign, ":best_body_val", ":score"),
                          (else_try),
                            (eq, ":item_type", itp_type_foot_armor),
                            (eq, ":upg_armor", 1), # we're uprgrading armor
                            (gt, ":score", ":best_boots_val"),
                            (assign, ":best_boots_slot", ":i_inventory"),
                            (assign, ":best_boots_val", ":score"),
                          (else_try),
                            (eq, ":item_type", itp_type_hand_armor),
                            (eq, ":upg_armor", 1), # we're uprgrading armor
                            (gt, ":score", ":best_gloves_val"),
                            (assign, ":best_gloves_slot", ":i_inventory"),
                            (assign, ":best_gloves_val", ":score"),
                          (try_end),
                        (try_end),

                        # equip best helmet
                        (try_begin),
                          (assign, ":best_slot", ":best_helmet_slot"),
                          (ge, ":best_slot", 0),
                          (troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
                          (ge, ":item", 0),
                          (troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
                          (troop_set_inventory_slot, ":troop", ek_head, ":item"),
                          (troop_set_inventory_slot_modifier, ":troop", ek_head, ":imod"),
                          (troop_set_inventory_slot, ":pool", ":best_slot", -1),
                        (try_end),

                        # equip best armor
                        (try_begin),
                          (assign, ":best_slot", ":best_body_slot"),
                          (ge, ":best_slot", 0),
                          (troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
                          (ge, ":item", 0),
                          (troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
                          (troop_set_inventory_slot, ":troop", ek_body, ":item"),
                          (troop_set_inventory_slot_modifier, ":troop", ek_body, ":imod"),
                          (troop_set_inventory_slot, ":pool", ":best_slot", -1),
                        (try_end),

                        # equip best boots
                        (try_begin),
                          (assign, ":best_slot", ":best_boots_slot"),
                          (ge, ":best_slot", 0),
                          (troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
                          (ge, ":item", 0),
                          (troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
                          (troop_set_inventory_slot, ":troop", ek_foot, ":item"),
                          (troop_set_inventory_slot_modifier, ":troop", ek_foot, ":imod"),
                          (troop_set_inventory_slot, ":pool", ":best_slot", -1),
                        (try_end),

                        # equip best gloves
                        (try_begin),
                          (assign, ":best_slot", ":best_gloves_slot"),
                          (ge, ":best_slot", 0),
                          (troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
                          (ge, ":item", 0),
                          (troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
                          (troop_set_inventory_slot, ":troop", ek_gloves, ":item"),
                          (troop_set_inventory_slot_modifier, ":troop", ek_gloves, ":imod"),
                          (troop_set_inventory_slot, ":pool", ":best_slot", -1),
                        (try_end),

                        # horse
                        (try_begin),
                          (assign, ":best_slot", ":best_horse_slot"),
                          (ge, ":best_slot", 0),
                          (troop_get_inventory_slot, ":item", ":pool", ":best_slot"),
                          (ge, ":item", 0),
                          (troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
                          (troop_set_inventory_slot, ":troop", ek_horse, ":item"),
                          (troop_set_inventory_slot_modifier, ":troop", ek_horse, ":imod"),
                          (troop_set_inventory_slot, ":pool", ":best_slot", -1),
                        (try_end),

                        # shields & weapons
                        (try_for_range, ":i_inventory", ek_item_0, ek_head),
                          (store_add, ":trp_slot", ":i_inventory", slot_troop_upgrade_wpn_0),
                          (troop_get_slot, ":upgrd", ":troop", ":trp_slot"),
                          (gt, ":upgrd", 0), #we're upgrading for this slot
                          (call_script, "script_scan_for_best_item_of_type", ":pool", ":upgrd", ":troop", ":require_mount_compatible"), #search for the best
                          (assign, ":best_slot", reg0),
                          (neq, ":best_slot", -1), #got something
                          (troop_get_inventory_slot, ":item", ":pool", ":best_slot"), #get it
                          (ge, ":item", 0),
                          (troop_get_inventory_slot_modifier, ":imod", ":pool", ":best_slot"),
                          (troop_set_inventory_slot, ":pool", ":best_slot", -1), #remove from pool
                          (troop_set_inventory_slot, ":troop", ":i_inventory", ":item"), #add to slot
                          (troop_set_inventory_slot_modifier, ":troop", ":i_inventory", ":imod"),
                        (try_end),
                      ]
                    ),
]
