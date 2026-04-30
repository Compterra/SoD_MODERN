SCRIPTS = [
("describe_land_quality",
                      [
                        (store_script_param, ":sreg", 1),
                        (store_script_param, ":village", 2),

                        (party_get_slot, ":quality", ":village", slot_village_land_quality),
                        (store_add, ":str_index", "str_land_quality_barren", ":quality"),
                        (str_store_string, ":sreg", ":str_index"),
                      ]
                    ),
]
