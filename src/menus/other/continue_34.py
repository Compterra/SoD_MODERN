MENUS = [
(
    "town_tournament_lost", 0,
    "You have been eliminated from the tournament.",
    "none",
    [
      (set_background_mesh, "mesh_pic_tournament"),
    ],
    [
      ("continue", [], "Continue...", [(jump_to_menu, "mnu_town_tournament_won_by_another"), ]),
    ]
  ),
]
