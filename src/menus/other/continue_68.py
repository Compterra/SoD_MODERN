MENUS = [
(
    "notification_troop_joined_players_faction", 0,
    "Good news!^^ {s1} has left {s2} and joined {s3}.",
    "none",
    [
      (call_script, "script_store_troop_name", s1, "$g_notification_menu_var1"),
      (str_store_faction_name, s2, "$g_notification_menu_var2"),
      (str_store_faction_name, s3, "$players_kingdom"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 55),
      (position_set_y, pos0, 20),
      (position_set_z, pos0, 100),
      (set_game_menu_tableau_mesh, "tableau_troop_note_mesh", "$g_notification_menu_var1", pos0),
      ],
    [
      ("continue", [], "Continue...",
       [(change_screen_return),
        ]),
     ]
  ),
]
