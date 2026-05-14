SCRIPTS = [
("determine_prisoner_agreed",
                      [
                        (store_script_param, ":prisoner", 1),
                        (store_script_param, ":relation", 2),

                        (try_begin),
                          (this_or_next|troop_is_hero, ":prisoner"),
                          (eq, ":prisoner", "trp_khergit_chieftain"),
                          (assign, ":reaction", 0),
                          (assign, ":upper_bound", 0),
                          (troop_set_slot, ":prisoner", slot_prisoner_agreed, 0),
                        (else_try),

                          # upper bound = Persuasion*3 + Charisma + Leadership*3 + Honor/2 - prisoner_level/3
                          (store_attribute_level, ":charisma", "trp_player", ca_charisma),
                          (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
                          (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
                          (val_mul, ":persuasion", 3),
                          (val_mul, ":leadership", 3),
                          (store_div, ":half_honor", "$player_honor", 2),
                          #(troop_get_slot, ":renown_factor", "trp_player", slot_troop_renown),
                          #(val_div, ":renown_factor", 100),
                          (store_character_level, ":prisoner_level", ":prisoner"),
                          (store_div, ":level_factor", ":prisoner_level", 3),
                          (assign,  ":upper_bound", ":persuasion"),
                          (val_add, ":upper_bound", ":leadership"),
                          (val_add, ":upper_bound", ":charisma"),
                          (val_add, ":upper_bound", ":half_honor"),
                          #(val_add, ":upper_bound", ":renown_factor"),
                          (val_sub, ":upper_bound", ":level_factor"),

                          # Larger prisoner stacks get proportionally more chances for one recruit to agree.
                          (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
                          (try_for_range, ":index", 0, ":num_stacks"),
                            (party_prisoner_stack_get_troop_id, ":troop_no", "p_main_party", ":index"),
                            (eq, ":troop_no", ":prisoner"),
                            (party_prisoner_stack_get_size, ":count", "p_main_party", ":index"),
                            (val_mul, ":upper_bound", ":count"),
                          (try_end),

                          (val_min, ":relation", ":upper_bound"),

                          # determine their reaction (relation...upper_bound)
                          (store_random_in_range, ":reaction", ":relation", ":upper_bound"),

                          # record whether they agree or not
                          (try_begin),
                            (gt, ":reaction", 0),
                            (troop_set_slot, ":prisoner", slot_prisoner_agreed, 1),
                          (else_try),
                            (troop_set_slot, ":prisoner", slot_prisoner_agreed, 0),
                          (try_end),
                        (try_end),

                        # return the results
                        (troop_get_slot, reg0, ":prisoner", slot_prisoner_agreed),

                        # diagnostic only
                        (try_begin),
                          (eq, "$g_sod_debug", 1),
                          (assign, reg1, ":reaction"),
                          (assign, reg2, ":relation"),
                          (assign, reg3, ":upper_bound"),
                          (display_message, "@Prisoner agrees check: rolled a {reg1} out of a possible {reg2}..{reg3} = {reg0?agree:piss off}", debug_color),
                        (try_end),
                      ]
                    ),
]
