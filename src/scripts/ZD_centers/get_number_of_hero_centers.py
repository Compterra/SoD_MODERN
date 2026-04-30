SCRIPTS = [
("get_number_of_hero_centers",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":result", 0),
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (val_add, ":result", 1),
      (try_end),
      (assign, reg0, ":result"),
  ]),
]
