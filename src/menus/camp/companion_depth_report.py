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
          (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
          (gt, ":num_stacks", 1),
        ], "Gather companions by the fire.",
        [
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
