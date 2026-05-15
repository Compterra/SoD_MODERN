MENUS = [
("companion_depth_report", mnf_scale_picture|mnf_enable_hot_keys,
   "{s1}",
   "none",
    [
      (set_background_mesh, "mesh_pic_camp"),
      (call_script, "script_sod_companion_describe_depth_report_to_s1"),
    ],
    [
      ("companion_depth_report_campfire", [
          (assign, ":has_companion", 0),
          (try_for_range, ":companion", companions_begin, companions_end),
            (main_party_has_troop, ":companion"),
            (assign, ":has_companion", 1),
          (try_end),
          (try_for_range, ":companion", special_companions_begin, special_companions_end),
            (main_party_has_troop, ":companion"),
            (assign, ":has_companion", 1),
          (try_end),
          (eq, ":has_companion", 1),
        ], "Gather companions by the fire.",
        [
          (assign, "$g_sod_companion_campfire_return_menu", "mnu_companion_depth_report"),
          (jump_to_menu, "mnu_companion_campfire"),
        ]
      ),
      ("companion_depth_report_back", [], "Return to camp actions.",
        [
          (jump_to_menu, "mnu_camp_action"),
        ]
      ),
    ]
  ),
]
