MENUS = [
("elite_doctrine_report", mnf_enable_hot_keys,
    "{s1}",
    "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),
      (call_script, "script_sod_describe_elite_doctrine_report"),
    ],
    [
      ("continue", [], "Continue.", [(jump_to_menu, "mnu_reports")]),
    ]
  ),
]
