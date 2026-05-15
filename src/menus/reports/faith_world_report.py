MENUS = [
("faith_world_report", mnf_enable_hot_keys,
    "{s1}",
    "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),
      (try_begin),
        (neq, "$cheat_mode", 1),
        (neq, "$g_sod_cheat_mode", 1),
        (jump_to_menu, "mnu_reports"),
      (try_end),
      (call_script, "script_sod_describe_faith_world_report"),
    ],
    [
      ("continue", [], "Continue.", [(jump_to_menu, "mnu_reports")]),
    ]
  ),
]
