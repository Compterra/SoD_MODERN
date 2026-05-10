MENUS = [
("noble_houses_report", mnf_enable_hot_keys,
    "{s1}",
    "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),
      (try_begin),
        (neq, "$g_sod_house_politics_active", 1),
        (call_script, "script_sod_initialize_house_identity"),
        (assign, "$g_sod_house_politics_active", 1),
      (try_end),
      (call_script, "script_sod_house_describe_noble_houses_to_s1"),
    ],
    [
      ("noble_houses_report_back", [], "Back to realm reports.", [(jump_to_menu, "mnu_realm_reports")]),
      ("noble_houses_report_resume", [], "Resume travelling.", [(change_screen_return)]),
    ]
  ),
]
