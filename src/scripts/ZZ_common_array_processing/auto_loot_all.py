SCRIPTS = [
("auto_loot_all",
                      [
                        (assign, ":debug", 1),

                        # get count of stacks in player's party
                        (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),

                        # record what items the npc used to have equipped in each slot
                        (try_for_range, ":i_stack", 0, ":num_stacks"),
                          (party_stack_get_troop_id, ":troop", "p_main_party", ":i_stack"),
                          (troop_slot_eq, ":troop", slot_troop_occupation, slto_player_companion),

                          #DEBUG
                          (try_begin),
                            (eq, ":debug", 2),
                            (call_script, "script_store_troop_name_link", s60, ":troop"),
                            (str_store_string, s1, "@{s60}'s equipment"),
                            (assign, ":debug_count", 0),
                          (try_end),

                          (try_for_range, ":i_equipment", ek_item_0, ek_food),

                            # store the original item
                            (troop_get_inventory_slot, ":item", ":troop", ":i_equipment"),
                            (store_add, ":i_troop_slot", ":i_equipment", slot_troop_item_0 - ek_item_0),
                            (troop_set_slot, ":troop", ":i_troop_slot", ":item"),

                            # store the original imod
                            (troop_get_inventory_slot_modifier, ":imod", ":troop", ":i_equipment"),
                            (store_add, ":i_troop_slot", ":i_equipment", slot_troop_item_0_imod - ek_item_0),
                            (troop_set_slot, ":troop", ":i_troop_slot", ":imod"),

                            #DEBUG
                            (try_begin),
                              (eq, ":debug", 2),
                              (try_begin),
                                (ge, ":item", 0),
                                (call_script, "script_describe_item_with_imod", s2, ":item", ":imod"),
                                (try_begin),
                                  (eq, ":debug_count", 0),
                                  (str_store_string, s1, "@{s1}: {s2}"),
                                (else_try),
                                  (str_store_string, s1, "@{s1}, {s2}"),
                                (try_end),
                                (val_add, ":debug_count", 1),
                              (try_end),
                            (try_end),

                            # make a determination of whether this npc should restrict themselves to mounted compatible equipment
                            (eq, ":i_equipment", ek_horse),
                            (try_begin),
                              # check if we're upgrading horses, or simply have one currently
                              (troop_get_slot, ":upg_horses", ":troop", slot_troop_upgrade_horse),
                              (this_or_next|eq, ":upg_horses", 1),
                              (ge, ":item", 0),
                              # only upgrade to items that can be used on horseback
                              (troop_set_slot, ":troop", slot_troop_restrict_mounted, 1),
                            (else_try),
                              # allow dismounted-only weapons & shield
                              (troop_set_slot, ":troop", slot_troop_restrict_mounted, 0),
                            (try_end),

                          (try_end), #(try_for_range, ":i_equipment", ek_item_0, ek_food),

                          #DEBUG
                          (try_begin),
                            (eq, ":debug", 2),
                            (gt, ":debug_count", 0),
                            (display_message, s1),
                          (try_end),

                        (try_end), #(try_for_range, ":i_stack", 0, ":num_stacks"),

                        # initial search for the best item available
                        (try_for_range, ":i_stack", 0, ":num_stacks"),
                          (party_stack_get_troop_id, ":troop", "p_main_party", ":i_stack"),
                          (troop_slot_eq, ":troop", slot_troop_occupation, slto_player_companion),
                          (troop_get_slot, ":require_mount_compatible", ":troop", slot_troop_restrict_mounted),
                          (call_script, "script_auto_loot_troop", ":troop", "$pool_troop", ":require_mount_compatible"),
                        (try_end),

                        # once more to pick up any discards
                        (try_for_range, ":i_stack", 0, ":num_stacks"),
                          (party_stack_get_troop_id, ":troop", "p_main_party", ":i_stack"),
                          (troop_slot_eq, ":troop", slot_troop_occupation, slto_player_companion),
                          (troop_get_slot, ":require_mount_compatible", ":troop", slot_troop_restrict_mounted),
                          (call_script, "script_auto_loot_troop", ":troop", "$pool_troop", ":require_mount_compatible"),
                        (try_end),

                        # a final time with relaxed settings to allow them to try to use horseback incompatible items IFF they didn't end up with a horse
                        (try_for_range, ":i_stack", 0, ":num_stacks"),
                          (party_stack_get_troop_id, ":troop", "p_main_party", ":i_stack"),
                          (troop_slot_eq, ":troop", slot_troop_occupation, slto_player_companion),

                          # only do this final step for those who were previously restricting themselves, and didn't find a horse
                          (troop_slot_eq, ":troop", slot_troop_restrict_mounted, 1),
                          (troop_slot_eq, ":troop", ek_horse, -1),
                          (call_script, "script_auto_loot_troop", ":troop", "$pool_troop", 0),
                        (try_end),

                        # accumulate the composite message of every change to every companion in s30
                        (str_clear, s30),
                        (assign, ":total", 0),
                        (try_for_range, ":i_stack", 0, ":num_stacks"),
                          (party_stack_get_troop_id, ":troop", "p_main_party", ":i_stack"),
                          (troop_slot_eq, ":troop", slot_troop_occupation, slto_player_companion),

                          # accumulate the text of all items this companion has newly equipped
                          (str_clear, s1),
                          (assign, ":changed", 0),
                          (try_for_range, ":i_equipment", ek_item_0, ek_food),
                            # retrieve the items
                            (store_add, ":i_troop_slot", ":i_equipment", slot_troop_item_0 - ek_item_0),
                            (troop_get_slot, ":old_item", ":troop", ":i_troop_slot"),
                            (troop_get_inventory_slot, ":new_item", ":troop", ":i_equipment"),

                            # retrieve the imods
                            (store_add, ":i_troop_slot", ":i_equipment", slot_troop_item_0_imod - ek_item_0),
                            (troop_get_slot, ":old_imod", ":troop", ":i_troop_slot"),
                            (troop_get_inventory_slot_modifier, ":new_imod", ":troop", ":i_equipment"),

                            # update our strings & count if this is not the same item as before
                            (ge, ":new_item", 0), # only report actual items, not the lack of an item
                            (this_or_next|neq, ":new_item", ":old_item"),
                            (             neq, ":new_imod", ":old_imod"),
                            (call_script, "script_describe_item_with_imod", s2, ":new_item", ":new_imod"),

                            (try_begin),
                              (ge, ":changed", 2),
                              (str_store_string, s1, "@{s2}, {s1}"),
                            (else_try),
                              (eq, ":changed", 1),
                              (str_store_string, s1, "@{s2}, and {s1}."),
                            (else_try),
                              (str_store_string, s1, "@{s2}"),
                            (try_end),
                            (val_add, ":changed", 1),

                            #DEBUG
                            (try_begin),
                              (eq, ":debug", 1),

                              (call_script, "script_describe_item_with_imod", s10, ":new_item", ":new_imod"),
                              (call_script, "script_get_item_score_with_imod", ":new_item", ":new_imod"),
                              (str_store_string, s10, "@{s10}({reg0})"),

                              (call_script, "script_describe_item_with_imod", s11, ":old_item", ":old_imod"),
                              (call_script, "script_get_item_score_with_imod", ":old_item", ":old_imod"),
                              (str_store_string, s11, "@{s11}({reg0})"),

                              (call_script, "script_store_troop_name_link", s12, ":troop"),
                              (display_message, "@{s12} replaced {s11} with {s10}", debug_color),
                            (try_end),
                          (try_end),

                          # append a message for this companion, if they equipped at least one new thing
                          (try_begin),
                            (gt, ":changed", 0),
                            (call_script, "script_store_troop_name_link", s2, ":troop"),
                            (str_store_string, s30, "@{s30}^{s2} equipped {s1}"),
                            (val_add, ":total", ":changed"),
                          (try_end),
                        (try_end),

                        # inform the player if nothing was exchanged
                        (try_begin),
                          (eq, ":total", 0),
                          (str_store_string, s30, "@^^^Unfortunately, there wasn't anything left worth equiping."),
                        (try_end),

                        # Done. Now sort the remainder
                        (troop_sort_inventory, "$pool_troop"),
                      ]
                    ),
]
