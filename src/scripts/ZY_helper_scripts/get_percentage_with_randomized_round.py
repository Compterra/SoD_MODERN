SCRIPTS = [
("get_percentage_with_randomized_round",
    [
      (store_script_param, ":value", 1),
      (store_script_param, ":percentage", 2),

      (store_mul, ":result", ":value", ":percentage"),
      (val_div, ":result", 100),
      (store_mul, ":used_amount", ":result", 100),
      (val_div, ":used_amount", ":percentage"),
      (store_sub, ":left_amount", ":value", ":used_amount"),
      (try_begin),
        (gt, ":left_amount", 0),
        (store_mul, ":chance", ":left_amount", ":percentage"),
        (store_random_in_range, ":random_no", 0, 100),
        (lt, ":random_no", ":chance"),
        (val_add, ":result", 1),
      (try_end),
      (assign, reg0, ":result"),
  ]),
]
