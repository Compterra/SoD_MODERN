MENUS = [
(
    "notification_one_faction_left", 0,
    "Calradia Conquered by One Kingdom^^{s1} has defeated all rivals and stands as the sole kingdom.",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (try_begin),
        (is_between, "$g_notification_menu_var1", "fac_kingdom_1", kingdoms_end), #Excluding player kingdom
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_for_menu", "$g_notification_menu_var1", pos0),
      (else_try),
        (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      (try_end),
      ],
    [
      ("continue", [], "Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
]
