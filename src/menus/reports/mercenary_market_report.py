MENUS = [
("mercenary_market_report", mnf_enable_hot_keys,
    "{s20}",
    "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),
      (call_script, "script_sod_merc_market_describe_overview_to_s20"),
    ],
    [
      ("mercenary_market_report_status", [], "View personal mercenary status.", [(jump_to_menu, "mnu_mercenary_status_report")]),
      ("mercenary_market_report_guilds", [], "View guild relations report.", [(jump_to_menu, "mnu_guilds_relations_report")]),
      ("mercenary_market_report_world", [], "Survey guild world activity.", [(jump_to_menu, "mnu_mercenary_world_activity_report")]),
      ("mercenary_market_report_back", [], "Back.", [(jump_to_menu, "mnu_mini_faction_reports")]),
    ]
  ),
]
