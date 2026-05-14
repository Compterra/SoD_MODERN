SCRIPTS = [
("change_player_honor",
    [
      (store_script_param_1, ":honor_dif"),
      (val_add, "$player_honor", ":honor_dif"),
      (try_begin),
        (gt, ":honor_dif", 0),
        (display_message, "@You gain honour.", honor_color),
      (else_try),
        (lt, ":honor_dif", 0),
        (display_message, "@You lose honour.", lose_honor_color),
      (try_end),
  ]),
]
