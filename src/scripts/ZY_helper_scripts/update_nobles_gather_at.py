SCRIPTS = [
("update_nobles_gather_at",
                      [
                        #(assign, reg0, "$g_sod_nobles_gather_at"),
                        #(display_message, "@update_nobles_gather_at: $g_sod_nobles_gather_at = {reg0}", debug_color),

                        # validate the current recruitment center, or clear it if its not valid anymore
                        (try_begin),
                          (neq, "$g_sod_nobles_gather_at", 0),
                          (store_faction_of_party, ":gather_faction", "$g_sod_nobles_gather_at"),
                          (this_or_next|neq, ":gather_faction", "fac_player_supporters_faction"),
                          (neg|party_slot_eq, "$g_sod_nobles_gather_at", slot_center_has_chapter, 1),
                          (assign, "$g_sod_nobles_gather_at", 0),
                          #(display_message, "@update_nobles_gather_at: resetting $g_sod_nobles_gather_at due to invalid current locale...", debug_color),
                        (try_end),

                        # assign aribtrary recruitment location if one hasn't been specified as yet
                        (try_begin),
                          (eq, "$g_sod_nobles_gather_at", 0),
                          (assign, ":best_center", 0),
                          (assign, ":best_score", -1),
                          (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
                            # must belong to the player's realm
                            (store_faction_of_party, ":center_faction", ":center_no"),
                            (eq, ":center_faction", "fac_player_supporters_faction"),
                            (party_slot_eq, ":center_no", slot_center_has_chapter, 1),

                            (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
                            (assign, ":score", ":prosperity"),
                            (try_begin),
                              (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
                              (val_add, ":score", 50),
                            (try_end),
                            (call_script, "script_sod_get_center_recruitment_policy", ":center_no"),
                            (store_mul, ":noble_recruitment_score", reg2, 5),
                            (val_add, ":score", ":noble_recruitment_score"),
                            (try_begin),
                              (party_slot_eq, ":center_no", slot_party_type, spt_town),
                              (val_add, ":score", 25),
                            (try_end),
                            (try_begin),
                              (gt, ":score", ":best_score"),
                              (assign, ":best_score", ":score"),
                              (assign, ":best_center", ":center_no"),
                            (try_end),
                          (try_end),
                          (try_begin),
                            (gt, ":best_center", 0),
                            (assign, "$g_sod_nobles_gather_at", ":best_center"),
                          (try_end),
                        (try_end),
                      ]
                    ),
]
