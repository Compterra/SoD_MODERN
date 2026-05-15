MENUS = [
("companion_campfire", mnf_scale_picture|mnf_enable_hot_keys,
   "{s68}",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (call_script, "script_sod_companion_describe_campfire_to_s68"),
    ],
    [
      ("companion_campfire_back", [], "Bank the fire and return.",
        [
          (try_begin),
            (gt, "$g_sod_companion_campfire_return_menu", 0),
            (assign, ":sod_campfire_back_menu", "$g_sod_companion_campfire_return_menu"),
            (assign, "$g_sod_companion_campfire_return_menu", 0),
            (jump_to_menu, ":sod_campfire_back_menu"),
          (else_try),
            (jump_to_menu, "mnu_camp_action"),
          (try_end),
        ]
      ),
    ]
  ),
]
