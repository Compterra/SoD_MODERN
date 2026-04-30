SCRIPTS = [
("get_closest_town_of_faction",
    [
      (store_script_param_1, ":party_no"),
      (store_script_param_2, ":kingdom_no"),
      (assign, ":min_distance", 9999999),
      (assign, ":result", -1),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (store_faction_of_party, ":faction_no", ":center_no"),
        (eq, ":faction_no", ":kingdom_no"),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (store_distance_to_party_from_party, ":party_distance", ":party_no", ":center_no"),
        (lt, ":party_distance", ":min_distance"),
        (assign, ":min_distance", ":party_distance"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
]
