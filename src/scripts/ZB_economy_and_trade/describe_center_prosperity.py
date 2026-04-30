SCRIPTS = [
("describe_center_prosperity",
                      [
                        (store_script_param, ":sreg", 1),
                        (store_script_param, ":center", 2),

                        (party_get_slot, ":prosperity", ":center", slot_town_prosperity),
                        (val_add, ":prosperity", 5),
                        (store_div, ":str_offset", ":prosperity", 10),
                        (val_clamp, ":str_offset", 0, 11), # BUG FIX: don't allow us to go beyond the range of messges (best is best, no further to go)
                        (try_begin),
                          (is_between, ":center", villages_begin, villages_end),
                          (store_add, ":str_id", "str_village_prosperity_0",  ":str_offset"),
                        (else_try),
                          (store_add, ":str_id", "str_town_prosperity_0",  ":str_offset"),
                        (try_end),
                        (str_store_party_name_link, s60, ":center"),
                        (str_store_string, ":sreg", ":str_id"),
                      ]
                    ),
]
