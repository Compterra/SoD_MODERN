MENUS = [
("camp", mnf_scale_picture|mnf_enable_hot_keys,
   "You set up camp. What do you want to do?",
   "none",
   [
     (assign, "$g_player_icon_state", pis_normal),
     (set_background_mesh, "mesh_pic_camp"),
    ],
    [
	
      ("kingdom_management", [(eq, "$g_sod_king", 1)], "Kingdom Management.", [(jump_to_menu, "mnu_kingdom_management")]),
      ("party_management", [], "Party Management.", [(jump_to_menu, "mnu_party_management")]),
	  ("sod_sa_menu",
        [(this_or_next|main_party_has_troop, "trp_sod_strategy_advisor"),
		 (eq, "$g_sod_sa_in_court", 1),
		],
        "Talk to the Strategy Advisor.",
        [
		(assign, "$sa_talk_after_siege", 0),
		(start_map_conversation, "trp_sod_strategy_advisor"),
		(change_screen_return),
       ]
      ),

      ("action_read_book", [], "Select a book to read.",
        [
          (jump_to_menu, "mnu_camp_action_read_book"),
        ]
       ),

      ("camp_wait_here", [], "Rest here for some time...",
       [
           (assign, "$g_camp_mode", 1),
           (assign, "$g_player_icon_state", pis_camping),
           (rest_for_hours_interactive, 24 * 7, 5, 1), #rest while attackable
           (change_screen_return),
        ]
       ),
      ("camp_action", [], "Take other action...", [(jump_to_menu, "mnu_camp_action")]),

      ("resume_travelling", [], "Resume travelling.", [(change_screen_return), ]), ]
  ),
]
