SCRIPTS = [
("get_item_score_with_imod",
                    [
                      (store_script_param, ":item", 1),
                      (store_script_param, ":imod", 2),

                      (assign, ":debug", 0),

                      (try_begin),
                        (eq, ":item", -1),
                        (assign, ":total_score", 0),
                      (else_try),
                        (item_get_type, ":type", ":item"),

                        # horse score = (armor + imod) * (speed + imod)
                        (eq, ":type", itp_type_horse),

                        (try_begin),
                          (eq, ":imod", imod_lame),
                          (assign, ":total_score", 0),

                          #DEBUG:
                          (try_begin),
                            (eq, ":debug", 1),
                            (display_message, "@...skipping lame horse", debug_color),
                          (try_end),

                        (else_try),

                          (item_get_slot, ":armor", ":item", slot_item_horse_armor),
                          (item_get_slot, ":imod_armor", ":imod", slot_item_imod_armor),
                          (store_add, ":total_armor", ":armor", ":imod_armor"),

                          (item_get_slot, ":speed", ":item", slot_item_horse_speed),
                          (item_get_slot, ":imod_speed", ":imod", slot_item_imod_speed),
                          (store_add, ":total_speed", ":speed", ":imod_speed"),

                          (store_mul, ":total_score", ":total_armor", ":total_speed"),

                          #DEBUG:
                          (try_begin),
                            (eq, ":debug", 1),
                            (assign, reg0, ":armor"),
                            (assign, reg1, ":imod_armor"),
                            (assign, reg2, ":speed"),
                            (assign, reg3, ":imod_speed"),
                            (assign, reg4, ":total_score"),
                            (display_message, "@horse score = (armor({reg0}) + imod({reg1}) * (speed({reg2}) + imod({reg3})) = {reg4}", debug_color),
                            (try_end),

                          (try_end),

                        (else_try),

                          # shield score = shield_size * (shield_armor + imod)
                          (eq, ":type", itp_type_shield),
                          (item_get_slot, ":size", ":item", slot_item_shield_size),
                          (item_get_slot, ":armor", ":item", slot_item_shield_armor),
                          (item_get_slot, ":imod_armor", ":imod", slot_item_imod_armor),
                          (store_add, ":total_armor", ":armor", ":imod_armor"),
                          (store_mul, ":total_score", ":size", ":total_armor"),

                          #DEBUG:
                          (try_begin),
                            (eq, ":debug", 1),
                            (assign, reg0, ":size"),
                            (assign, reg2, ":armor"),
                            (assign, reg3, ":imod_armor"),
                            (assign, reg4, ":total_score"),
                            (display_message, "@shield score = size({reg0}) * (armor({reg2}) + imod({reg3})) = {reg4}", debug_color),
                          (try_end),

                        (else_try),

                          # armor score = (head_armor + imod) + (body_armor + imod) + (leg_armor + imod)
                          (this_or_next|eq, ":type", itp_type_head_armor),
                          (this_or_next|eq, ":type", itp_type_body_armor),
                          (this_or_next|eq, ":type", itp_type_foot_armor),
                          (             eq, ":type", itp_type_hand_armor),

                          # get the imod effect on armor
                          (item_get_slot, ":imod_armor", ":imod", slot_item_imod_armor),

                          # get the adjusted armor value of each aspect of this armor
                          (item_get_slot, ":head_armor", ":item", slot_item_head_armor),
                          (try_begin),
                            (gt, ":head_armor", 0),
                            (store_add, ":total_head_armor", ":head_armor", ":imod_armor"),
                          (else_try),
                            (assign, ":total_head_armor", ":head_armor"),
                          (try_end),

                          (item_get_slot, ":body_armor", ":item", slot_item_body_armor),
                          (try_begin),
                            (gt, ":body_armor", 0),
                            (store_add, ":total_body_armor", ":body_armor", ":imod_armor"),
                          (else_try),
                            (assign, ":total_body_armor", ":body_armor"),
                          (try_end),

                          (item_get_slot, ":leg_armor", ":item", slot_item_leg_armor),
                          (try_begin),
                            (gt, ":leg_armor", 0),
                            (store_add, ":total_leg_armor", ":leg_armor", ":imod_armor"),
                          (else_try),
                            (assign, ":total_leg_armor", ":leg_armor"),
                          (try_end),

                          # add all of the adjusted armors together
                          (assign, ":total_score", ":total_head_armor"),
                          (val_add, ":total_score", ":total_body_armor"),
                          (val_add, ":total_score", ":total_leg_armor"),

                          #DEBUG:
                          (try_begin),
                            (eq, ":debug", 1),
                            (assign, reg0, ":head_armor"),
                            (assign, reg1, ":body_armor"),
                            (assign, reg2, ":leg_armor"),
                            (assign, reg3, ":imod_armor"),
                            (assign, reg4, ":total_score"),
                            (display_message, "@armor score = (head_armor({reg0}) + imod({reg3})) + (body_armor({reg1}) + imod({reg3})) + (leg_armor({reg2}) + imod({reg3})) = {reg4}", debug_color),
                          (try_end),

                        (else_try),

                          # weapon score = max((swing_damage * dmg_type_adj_factor), (thrust_damage * dmg_type_adj_factor))
                          (this_or_next|eq, ":type", itp_type_one_handed_wpn),
                          (this_or_next|eq, ":type", itp_type_two_handed_wpn),
                          (this_or_next|eq, ":type", itp_type_bow),
                          (this_or_next|eq, ":type", itp_type_crossbow),
                          (             eq, ":type", itp_type_polearm),

                          # get the imod first - it adjusts the base damage value
                          (item_get_slot, ":imod_damage", ":imod", slot_item_imod_damage),

                          # get actual damage values adjusted for damage type
                          (item_get_slot, ":swing_damage", ":item", slot_item_swing_damage),
                          (store_add, ":total_swing_damage", ":swing_damage", ":imod_damage"),
                          (item_get_slot, ":swing_damage_type", ":item", slot_item_swing_damage_type),
                          (call_script, "script_get_damage_adjusted_for_type", ":total_swing_damage", ":swing_damage_type"),
                          (assign, ":total_swing_damage", reg0),

                          (item_get_slot, ":thrust_damage", ":item", slot_item_thrust_damage),
                          (store_add, ":total_thrust_damage", ":thrust_damage", ":imod_damage"),
                          (item_get_slot, ":thrust_damage_type", ":item", slot_item_thrust_damage_type),
                          (call_script, "script_get_damage_adjusted_for_type", ":total_thrust_damage", ":thrust_damage_type"),
                          (assign, ":total_thrust_damage", reg0),

                          # use the better of the two as the basis for choosing to upgrade to this weapon
                          (assign, ":total_score", ":total_swing_damage"),
                          (val_max, ":total_score", ":total_thrust_damage"),

                          #DEBUG:
                          (try_begin),
                            (eq, ":debug", 1),
                            (assign, reg0, ":swing_damage"),
                            (assign, reg1, ":thrust_damage"),
                            #(assign, reg2, ":leg_armor"),
                            (assign, reg3, ":imod_damage"),
                            (assign, reg4, ":total_score"),
                            (display_message, "@weapon score = max(swing_damage({reg0})+imod({reg3}), thrust_damage({reg1})+imod({reg3})) ~= {reg4}", debug_color),
                          (try_end),

                        (else_try),

                          # missiles score = (thrust damage + imod_damage) * 2 (+1 if large bag)
                          (this_or_next|eq, ":type", itp_type_arrows),
                          (this_or_next|eq, ":type", itp_type_bolts),
                          (             eq, ":type", itp_type_thrown),

                          (item_get_slot, ":thrust_damage", ":item", slot_item_thrust_damage),
                          (item_get_slot, ":imod_damage", ":imod", slot_item_imod_damage),
                          (store_add, ":total_score", ":thrust_damage", ":imod_damage"),

                          # a_large_bag will add 1 to score to discriminate the same ammo with the plain modifier
                          (try_begin),
                            (eq, ":imod", imod_large_bag),
                            (val_add, ":total_score", 1),
                          (try_end),

                        (try_end),

                        (assign, reg0, ":total_score"),
                      ]
                    ),
]
