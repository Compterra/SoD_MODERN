SCRIPTS = [
("update_party_creation_random_limits",
    [
      (store_character_level, ":player_level", "trp_player"),
      (store_mul, ":upper_limit", ":player_level", 3),
      (val_add, ":upper_limit", 25),
      (val_min, ":upper_limit", 100),
      (set_party_creation_random_limits, 0, ":upper_limit"),
      (assign, reg0, ":upper_limit"),
  ]),
]
