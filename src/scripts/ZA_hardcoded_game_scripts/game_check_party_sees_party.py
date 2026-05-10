SCRIPTS = [
("game_check_party_sees_party",
    [
      (store_script_param_1, ":viewer_party"),
      (store_script_param_2, ":seen_party"),
      (assign, reg0, 1),
      (try_begin),
        (lt, ":viewer_party", 0),
        (assign, reg0, 0),
      (else_try),
        (lt, ":seen_party", 0),
        (assign, reg0, 0),
      (try_end),
      (set_trigger_result, reg0),
    ]),
]
