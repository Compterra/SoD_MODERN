SCRIPTS = [
("game_check_prisoner_can_be_sold",
    [
      (store_script_param_1, ":troop_id"),
      (assign, reg0, 0),
      (try_begin),
        (neg|troop_is_hero, ":troop_id"),
        (is_between, ":troop_id", soldiers_begin, soldiers_end),
        (assign, reg0, 1),
      (try_end),
      (set_trigger_result, reg0),
  ]),
]
