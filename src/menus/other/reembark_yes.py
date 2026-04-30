MENUS = [
(
    "ship_reembark", 0,
    "Do you wish to embark?",
    "none",
    [],
    [
      ("reembark_yes", [], "Yes.",
       [(assign, "$g_player_icon_state", pis_ship),
        (party_set_flags, "p_main_party", pf_is_ship, 1),
        (party_get_position, pos1, "p_main_party"),
        (map_get_water_position_around_position, pos2, pos1, 6),
        (party_set_position, "p_main_party", pos2),
        (assign, "$g_main_ship_party", "$g_encountered_party"),
        (disable_party, "$g_encountered_party"),
        (change_screen_return),
        ]),
      ("reembark_no", [], "No.",
       [(change_screen_return),
        ]),
    ]
  ),
]
