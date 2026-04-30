SCRIPTS = [
("game_get_money_text",
    [
      (store_script_param_1, ":amount"),
      (try_begin),
        (eq, ":amount", 1),
        (str_store_string, s1, "str_1_denar"),
      (else_try),
        (assign, reg1, ":amount"),
        (str_store_string, s1, "str_reg1_denars"),
      (try_end),
      (set_result_string, s1),
  ]),
]
