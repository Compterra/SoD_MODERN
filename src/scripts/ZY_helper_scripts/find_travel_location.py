SCRIPTS = [
("find_travel_location",
    [
      (store_script_param_1, ":center_no"),
      (store_faction_of_party, ":faction_no", ":center_no"),
      (assign, ":total_weight", 0),
      (try_for_range, ":cur_center_no", centers_begin, centers_end),
        (neq, ":center_no", ":cur_center_no"),
        (store_faction_of_party, ":center_faction_no", ":cur_center_no"),
        (eq, ":faction_no", ":center_faction_no"),

        (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":cur_center_no"),
        (val_add, ":cur_distance", 1),

        (assign, ":new_weight", 100000),
        (val_div, ":new_weight", ":cur_distance"),
        (val_add, ":total_weight", ":new_weight"),
      (try_end),

      (assign, reg0, -1),

      (try_begin),
        (eq, ":total_weight", 0),
      (else_try),
        (store_random_in_range, ":random_weight", 0 , ":total_weight"),
        (assign, ":total_weight", 0),
        (assign, ":done", 0),
        (try_for_range, ":cur_center_no", centers_begin, centers_end),
          (eq, ":done", 0),
          (neq, ":center_no", ":cur_center_no"),
          (store_faction_of_party, ":center_faction_no", ":cur_center_no"),
          (eq, ":faction_no", ":center_faction_no"),

          (store_distance_to_party_from_party, ":cur_distance", ":center_no", ":cur_center_no"),
          (val_add, ":cur_distance", 1),

          (assign, ":new_weight", 100000),
          (val_div, ":new_weight", ":cur_distance"),
          (val_add, ":total_weight", ":new_weight"),
          (lt, ":random_weight", ":total_weight"),
          (assign, reg0, ":cur_center_no"),
          (assign, ":done", 1),
        (try_end),
      (try_end),
  ]),
]
