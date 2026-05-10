MENUS = [
("trade_network_report", mnf_enable_hot_keys,
    "{s1}",
    "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),
      (call_script, "script_sod_trade_network_describe_report_to_s20"),
      (str_store_string, s1, "@{s20}"),
    ],
    [
      ("trade_network_report_back", [], "Back to reports.", [(jump_to_menu, "mnu_reports")]),
    ]
  ),
]
