MENUS = [
(
    "ship_reembark", 0,
    "Do you wish to embark?",
    "none",
    [],
    [
      ("reembark_yes", [
        (gt, "$g_encountered_party", 0),
        (neq, "$g_encountered_party", "p_main_party"),
        (party_is_active, "$g_encountered_party"),
        (party_slot_eq, "$g_encountered_party", slot_party_type, spt_ship),
        ], "Yes.",
       [(assign, "$g_player_icon_state", pis_ship),
        (party_set_flags, "p_main_party", pf_is_ship, 1),
        (call_script, "script_sod_refresh_player_map_icon"),
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
