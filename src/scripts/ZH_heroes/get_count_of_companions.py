SCRIPTS = [
("get_count_of_companions",
                      [
                        (assign, reg0, 0),
                        (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
                        (try_for_range, ":i_stack", 0, ":num_stacks"),
                          (party_stack_get_troop_id, ":this_hero", "p_main_party", ":i_stack"),
                          (troop_slot_eq, ":this_hero", slot_troop_occupation, slto_player_companion),
                          (val_add, reg0, 1),
                        (end_try),
                      ]
                    ),
]
