SCRIPTS = [
("cf_select_random_town_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (assign, ":result", -1),

      # First count num matching spawn points
      (assign, ":no_towns", 0),
      (try_for_range, ":cur_town", towns_begin, towns_end),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_towns", 1),
      (try_end),
      (gt, ":no_towns", 0), #Fail if there are no towns
      (store_random_in_range, ":random_town", 0, ":no_towns"),
      (assign, ":no_towns", 0),
      (try_for_range, ":cur_town", towns_begin, towns_end),
        (eq, ":result", -1),
        (store_faction_of_party, ":cur_faction", ":cur_town"),
        (eq, ":cur_faction", ":faction_no"),
        (val_add, ":no_towns", 1),
        (gt, ":no_towns", ":random_town"),
        (assign, ":result", ":cur_town"),
      (try_end),
      (assign, reg0, ":result"),
  ]),
]
