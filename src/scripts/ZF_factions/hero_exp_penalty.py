SCRIPTS = [
("hero_exp_penalty",
                      [
                        (store_character_level, ":level", "trp_player"),
                        (val_mul, ":level", -20),
                        (add_xp_to_troop, ":level", "trp_player"),
                        (assign, reg1, ":level"),
                        (display_message, "@You lost {reg1} experience points.", 0x8fbc8f),
                      ]
                    ),
]
