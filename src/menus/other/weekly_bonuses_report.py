MENUS = [
("weekly_bonuses_report", mnf_enable_hot_keys,
    "{s1}",
    "none",
    [
		(set_background_mesh, "mesh_pic_report_screen"),
		(call_script, "script_sod_law_migrate_player_legacy_slots"),
		
		(faction_get_slot, reg1, "fac_player_supporters_faction", slot_faction_law_village_relation_modifier),
		(faction_get_slot, reg2, "fac_player_supporters_faction", slot_faction_law_town_relation_modifier),
		(faction_get_slot, reg3, "fac_player_supporters_faction", slot_faction_law_village_prosperity_modifier),
		(faction_get_slot, reg4, "fac_player_supporters_faction", slot_faction_law_town_prosperity_modifier),
		(faction_get_slot, reg5, "fac_player_supporters_faction", slot_faction_law_noble_happiness),
		(faction_get_slot, reg6, "fac_player_supporters_faction", slot_faction_law_clergy_happiness),
		(faction_get_slot, reg7, "fac_player_supporters_faction", slot_faction_law_village_faith_modifier),
		(faction_get_slot, reg8, "fac_player_supporters_faction", slot_faction_law_town_faith_modifier),
		(assign, reg9, "$g_sod_renown_modifier"),
		
		(str_store_string, s1, "@Weekly realm law modifiers...^"),
		(str_store_string, s1, "@{s1}Relations with villages: {reg1}^"),
		(str_store_string, s1, "@{s1}Relations with towns: {reg2}^"),
		(str_store_string, s1, "@{s1}Village prosperity growth: {reg3}^"),
		(str_store_string, s1, "@{s1}Town prosperity growth: {reg4}^"),
		(str_store_string, s1, "@{s1}Nobility happiness: {reg5}^"),
		(str_store_string, s1, "@{s1}Clergy happiness: {reg6}^"),
		(str_store_string, s1, "@{s1}Village local faith growth: {reg7}^"),
		(str_store_string, s1, "@{s1}Town local faith growth: {reg8}^"),
		(str_store_string, s1, "@{s1}Renown: {reg9}^"),
    ],
    [
      ("view_lord_other", [], "Let me see a different report...", [(jump_to_menu, "mnu_reports")]),
      ("view_lord_travel", [], "Resume travelling.", [(change_screen_return)]),
    ]
  ),
]
