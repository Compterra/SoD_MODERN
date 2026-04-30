MENUS = [
("retirement_verify", mnf_scale_picture|mnf_enable_hot_keys,
   "You are at day {reg0}. Your current luck is {reg1}.^^Are you sure you want to retire?",
   "none",
    [
      (set_background_mesh, "mesh_pic_defeat"),
      (store_current_day, reg0),
      (assign, reg1, "$g_player_luck"),
    ],
    [
      ("retire_yes", [], "Yes.",
        [
          (start_presentation, "prsnt_retirement"),
        ]
      ),
      ("retire_no", [], "No.",
        [
         (jump_to_menu, "mnu_camp"),
        ]
      ),
    ]
  ),
]
