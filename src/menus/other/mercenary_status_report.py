MENUS = [
("mercenary_status_report", mnf_enable_hot_keys,
    "{s1}",
    "none",
    [
      (set_background_mesh, "mesh_pic_report_screen"),
      (call_script, "script_merc_describe_report_summary"),
      (call_script, "script_merc_describe_contract_board"),
      (str_store_string, s1, "@Mercenary Service Board^^{s63}^^{s64}^^{s65}^^{s66}^^{s67}^^Mercenary Ledger^^{s60}^^{s61}^^{s62}"),
    ],
    [
      ("view_mercenary_market_report", [], "Read the guild market ledger.", [(jump_to_menu, "mnu_mercenary_market_report")]),
      ("view_guild_relations_report", [], "View guild relations report.", [(jump_to_menu, "mnu_guilds_relations_report")]),
      ("view_reports", [], "Let me see a different report...", [(jump_to_menu, "mnu_reports")]),
      ("resume_travelling", [], "Resume travelling.", [(change_screen_return)]),
    ]
  ),
]
