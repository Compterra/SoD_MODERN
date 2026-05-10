SCRIPTS = [
("get_closest_town",
    [
      (store_script_param_1, ":party_no"),
      (assign, ":min_distance", 9999999),
      (assign, reg0, -1),
      (try_begin),
        (gt, ":party_no", 0),
        (party_is_active, ":party_no"),
        (try_for_range, ":center_no", towns_begin, towns_end),
          (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
          (lt, ":party_distance", ":min_distance"),
          (assign, ":min_distance", ":party_distance"),
          (assign, reg0, ":center_no"),
        (try_end),
      (try_end),
  ]),
]
