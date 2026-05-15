MENUS = [
("training_ground_description", 0,
   "{s68}",
   "none",
   [],
    [
      ("continue", [], "Continue...",
       [
         (set_jump_mission, "mt_training_ground_training"),
         (jump_to_scene, "$g_training_ground_training_scene"),
         (change_screen_mission),
        ]
       ),
      ]
  ),
]
