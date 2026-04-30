MENUS = [
(
    "notification_new_king", 0,
    "^^^ {s1} is the new ruler of {s2}.",
    "none",
    [
      (call_script, "script_store_troop_name", s1, "$new_king"),
      (str_store_faction_name, s2, "$kingdom_with_new_king"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 55),
      (position_set_y, pos0, 20),
      (position_set_z, pos0, 100),
      (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", "$new_king", pos0),
      ],
    [
      ("continue", [], "Continue...",
       [(assign, "$event_new_king", 0),
	   (change_screen_return),
        ]),
     ]
  ),
]
