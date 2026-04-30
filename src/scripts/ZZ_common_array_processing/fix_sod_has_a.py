SCRIPTS = [
("fix_sod_has_a",
                      [
                        (store_script_param, ":center", 1),
                        (store_script_param, ":building_start", 2),
                        (store_script_param, ":offset", 3),

                        # adjust to be zero based
                        (val_sub, ":offset", 1),

                        # one past end
                        (store_add, ":building_end", ":building_start", 5),

                        # fix existing building of this type
                        (assign, ":has_a", 0),
                        (try_for_range, ":building", ":building_start", ":building_end"),
                          (party_slot_ge, ":center", ":building", 1),
                          (assign, ":has_a", 1),
                          (party_set_slot, ":center", ":building", 0),
                        (try_end),
                        (store_add, ":building", ":building_start", ":offset"),
                        (party_set_slot, ":center", ":building", ":has_a"),

                        # fix under construction building of this type
                        (party_get_slot, ":building", ":center", slot_center_current_improvement),
                        (try_begin),
                          (is_between, ":building", ":building_start", ":building_end"),
                          (store_add, ":building", ":building_start", ":offset"),
                          (party_set_slot, ":center", slot_center_current_improvement, ":building"),
                        (try_end),
                      ]
                    ),
]
