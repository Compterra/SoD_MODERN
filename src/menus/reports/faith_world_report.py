MENUS = [
("faith_world_report", mnf_enable_hot_keys,
    "{s1}",
    "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),
      (call_script, "script_sod_describe_faith_world_report"),
    ],
    [
      ("continue", [], "Continue.", [(jump_to_menu, "mnu_reports")]),
    ]
  ),
]
