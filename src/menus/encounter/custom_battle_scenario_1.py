MENUS = [
(
    "start_game_3", mnf_disable_all_keys,
    "Choose your scenario:",
    "none",
    [
      #Default banners
      (troop_set_slot, "trp_banner_background_color_array", 126, 0xFF212221),
      (troop_set_slot, "trp_banner_background_color_array", 127, 0xFF212221),
      (troop_set_slot, "trp_banner_background_color_array", 128, 0xFF2E3B10),
      (troop_set_slot, "trp_banner_background_color_array", 129, 0xFF425D7B),
      (troop_set_slot, "trp_banner_background_color_array", 130, 0xFF394608),
      ],
    [
      ("custom_battle_scenario_1", [], "Skirmish 1",
       [
           (assign, "$g_custom_battle_scenario", 0),
           (jump_to_menu, "mnu_custom_battle_2"),

        ]
       ),
##      ("custom_battle_scenario_2", [], "Siege Attack 1",
##       [
##           (assign, "$g_custom_battle_scenario", 1),
##           (jump_to_menu, "mnu_custom_battle_2"),
##
##        ]
##       ),
      ("custom_battle_scenario_3", [], "Skirmish 2",
       [
           (assign, "$g_custom_battle_scenario", 1),
           (jump_to_menu, "mnu_custom_battle_2"),

        ]
       ),
       ("custom_battle_scenario_4", [], "Siege Defense",
       [
           (assign, "$g_custom_battle_scenario", 2),
           (jump_to_menu, "mnu_custom_battle_2"),
        ]
       ),
       ("custom_battle_scenario_5", [], "Skirmish 3",
       [
           (assign, "$g_custom_battle_scenario", 3),
           (jump_to_menu, "mnu_custom_battle_2"),
        ]
       ),
      ("custom_battle_scenario_6", [], "Siege Attack",
       [
           (assign, "$g_custom_battle_scenario", 4),
           (jump_to_menu, "mnu_custom_battle_2"),

        ]
       ),
      ("go_back", [], "Go back",
       [(change_screen_quit),
        ]
       ),
    ]
  ),
]
