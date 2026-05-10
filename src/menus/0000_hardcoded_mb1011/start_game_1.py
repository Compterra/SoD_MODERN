MENUS = [
(
    "start_game_1", mnf_disable_all_keys,
    "Welcome, adventurer, to Mount&Blade. Before you can start playing the game you must create a character. To begin, select your character's gender.",
    "none",
    [
      (set_background_mesh, "mesh_pic_chr1_gender"),
    ],
    [
      ("start_male", [], "Male",
       [
           (troop_set_type, "trp_player", 0),
           (assign, "$character_gender", tf_male),
           (jump_to_menu, "mnu_start_character_1"),
        ]
       ),
      ("start_female", [], "Female",
       [
           (troop_set_type, "trp_player", 1),
           (assign, "$character_gender", tf_female),
           (jump_to_menu, "mnu_start_character_1")
        ]
       ),
      ("go_back", [], "Go back",
       [(change_screen_quit),
        ]
       ),
      ]
  ),
]
