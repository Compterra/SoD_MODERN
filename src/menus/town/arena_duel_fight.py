MENUS = [
("arena_duel_fight", 0,
   "You and your opponent prepare to fight for honour.",
   "none",
   [],
   [
     ("continue", [], "Continue...",
      [
        (jump_to_menu, "mnu_simple_encounter"),
        (change_screen_mission),
        ]),
      ]
  ),
]
