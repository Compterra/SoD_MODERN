SCRIPTS = [
("game_event_context_menu_button_clicked",
    [(store_script_param, ":party_no", 1),
      (store_script_param, ":button_value", 2),
      (try_begin),
        (eq, ":button_value", 1),
        (change_screen_notes, 3, ":party_no"),
      (else_try),
        (eq, ":button_value", 2),
        (party_stack_get_troop_id, ":troop_no", ":party_no", 0),
        (change_screen_notes, 1, ":troop_no"),
      (try_end),
  ]),
]
