SCRIPTS = [
("troop_get_leaded_center_with_index",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":random_center"),
      (assign, ":result", -1),
      (assign, ":center_count", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (eq, ":result", -1),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (val_add, ":center_count", 1),
        (gt, ":center_count", ":random_center"),
        (assign, ":result", ":center_no"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
]
