MENUS = [
(
    "notification_player_faction_active", 0,
    "You now posess land in your name without being tied to any kingdom, as a masterless warlord who knows no higher authority."\
    " Enjoy this freedom, but know that the kings of the land will not look to you kindly and will make every attempt to dispose of you."\
    " You may find life very difficult without the protection of a kingdom.",
    "none",
    [
      (set_background_mesh, "mesh_pic_kingdom"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "fac_player_supporters_faction", pos0),
    ],
    [
      ("continue", [], "Continue...",
       [
	   (try_begin),
		(main_party_has_troop, "trp_sod_strategy_advisor"),
		(assign, "$sa_talk_after_siege", 1),
		(start_map_conversation, "trp_sod_strategy_advisor"),
		(change_screen_return),
	   (else_try),
		(change_screen_return),
	   (try_end),
        ]),
     ]
  ),
]
