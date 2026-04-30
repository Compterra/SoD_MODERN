SCRIPTS = [
("troop_can_use_item",
                    [
                      (store_script_param, ":troop", 1),
                      (store_script_param, ":item", 2),
                      (store_script_param, ":imod", 3),

                      (item_get_slot, ":difficulty", ":item", slot_item_difficulty),

                      (try_begin),

                        # anyone can use this item
                        (eq, ":difficulty", 0),
                        (assign, reg0, 1),

                      (else_try),

                        # adjust for imod
                        (item_get_slot, ":adj", ":imod", slot_item_imod_require),
                        (val_add, ":difficulty", ":adj"),

                        # determine which skill or attribute the difficulty rating applies to
                        (item_get_type, ":type", ":item"),
                        (try_begin),
                          # horse (skl_riding)
                          (eq, ":type", itp_type_horse),
                          (store_skill_level, ":skill", skl_riding, ":troop"),
                        (else_try),
                          # melee weapon or armor (strength)
                          (this_or_next|eq, ":type", itp_type_crossbow),
                          (this_or_next|eq, ":type", itp_type_one_handed_wpn),
                          (this_or_next|eq, ":type", itp_type_two_handed_wpn),
                          (this_or_next|eq, ":type", itp_type_polearm),
                          (this_or_next|eq, ":type", itp_type_head_armor),
                          (this_or_next|eq, ":type", itp_type_body_armor),
                          (this_or_next|eq, ":type", itp_type_foot_armor),
                          (             eq, ":type", itp_type_hand_armor),
                          (store_attribute_level, ":skill", ":troop", ca_strength),
                        (else_try),
                          # shield (skl_shield)
                          (eq, ":type", itp_type_shield),
                          (store_skill_level, ":skill", skl_shield, ":troop"),
                        (else_try),
                          # bow (power draw)
                          (eq, ":type", itp_type_bow),
                          (store_skill_level, ":skill", skl_power_draw, ":troop"),
                        (else_try),
                          # thrown weapon (power throw)
                          (eq, ":type", itp_type_thrown),
                          (store_skill_level, ":skill", skl_power_throw, ":troop"),
                        (try_end),

                        (try_begin),
                          # check if the troop has enough skill to equip this item
                          (ge, ":skill", ":difficulty"),
                          (assign, reg0, 1),
                        (else_try),
                          (assign, reg0, 0),
                        (try_end),
                      (try_end),
                    ]
                  ),
]
