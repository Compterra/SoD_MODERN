SCRIPTS = [
("map_get_random_position_around_position_within_range",
    [
      (store_script_param_1, ":min_distance"),
      (store_script_param_2, ":max_distance"),
      (val_mul, ":min_distance", 100),
      (assign, ":continue", 1),
      (try_for_range, ":unused", 0, 20),
        (eq, ":continue", 1),
        (map_get_random_position_around_position, pos2, pos1, ":max_distance"),
        (get_distance_between_positions, ":distance", pos2, pos1),
        (ge, ":distance", ":min_distance"),
        (assign, ":continue", 0),
      (try_end),
  ]),
]
