MENUS = [
(
    "sneak_into_town_caught_dispersed_guards", 0,
    "You drive off the guards and cover your trail before running off, easily losing your pursuers in the maze of streets.",
    "none",
    [
      (set_background_mesh, "$g_sod_town_background"),
    ],
    [
      ("continue", [], "Continue...",
        [
          (assign, "$sneaked_into_town", 1),
          (assign, "$town_entered", 1),
          (jump_to_menu, "mnu_town"),
        ]
      ),
    ]
  ),
]
