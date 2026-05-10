MENUS = [
("realm_law_report", mnf_enable_hot_keys,
    "{s1}",
    "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),
      (call_script, "script_sod_law_describe_realm_law_report"),
    ],
    [
      ("continue", [], "Continue.", [(jump_to_menu, "mnu_reports")]),
    ]
  ),
]
