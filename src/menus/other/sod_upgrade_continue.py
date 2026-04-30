MENUS = [
("sod_upgrade_continue", 0,
	"You have {reg4} denars.^^Choose a doctrine path for your {reg5} {s3}.{s4}",
	"none", [
		(store_troop_gold, reg4, "trp_player"),
		(party_count_companions_of_type, reg5, "p_main_party", "$g_sod_town_upgrade_selected_troop"),
		(assign, "$upgrade_count", reg5),
		(try_begin),
			(eq, "$upgrade_count", 0),
			(try_begin),
				(neq, "$g_encountered_party", -1),
				(jump_to_menu, "mnu_sod_upgrade"),
			(else_try),
				(jump_to_menu, "mnu_sod_upgrade_camp"),
			(try_end),
		(try_end),
		(str_store_troop_name_by_count, s3, "$g_sod_town_upgrade_selected_troop", reg5),
		(str_clear, s4),
		
		(troop_get_slot, ":upgrade1", "$g_sod_town_upgrade_selected_troop", slot_troop_sod_upgrade1),
		(call_script, "script_sod_can_upgrade_troops_here", ":upgrade1", "$g_encountered_party"),
		(assign, "$can_upgrade1", reg0),
		(troop_get_slot, ":upgrade2", "$g_sod_town_upgrade_selected_troop", slot_troop_sod_upgrade2),
		(call_script, "script_sod_can_upgrade_troops_here", ":upgrade2", "$g_encountered_party"),
		(assign, "$can_upgrade2", reg0),
		(try_begin),
			(eq, "$can_upgrade1", 1),
			(call_script, "script_sod_troop_get_elite_tier", ":upgrade1"),
			(try_begin),
				(eq, reg0, sod_elite_tier_faith),
				(str_store_string, s4, "@^^Elite doctrine: Faith ascension. This is the highest troop tier and requires chapel or temple support."),
			(else_try),
				(eq, reg0, sod_elite_tier_noble),
				(str_store_string, s4, "@^^Elite doctrine: Noble house training. Nobles are the second-best troop tier and require chapter support."),
			(try_end),
		(else_try),
			(eq, "$can_upgrade2", 1),
			(call_script, "script_sod_troop_get_elite_tier", ":upgrade2"),
			(try_begin),
				(eq, reg0, sod_elite_tier_faith),
				(str_store_string, s4, "@^^Elite doctrine: Faith ascension. This is the highest troop tier and requires chapel or temple support."),
			(else_try),
				(eq, reg0, sod_elite_tier_noble),
				(str_store_string, s4, "@^^Elite doctrine: Noble house training. Nobles are the second-best troop tier and require chapter support."),
			(try_end),
		(try_end),
		(assign, "$g_upgrade_troop", "$g_sod_town_upgrade_selected_troop"),
	],
	[	
		# Upgrade all to upgrade1
  ("marshal_upgrade_choose1",
    [
      (eq, "$can_upgrade1", 1),
      (gt, "$upgrade_count", 1),
      (neq, "$upgrade_count", 5),

      (troop_get_slot, ":upgrade1", "$g_upgrade_troop", slot_troop_sod_upgrade1),

      (str_store_troop_name_by_count, s1, "$g_upgrade_troop", "$upgrade_count"),
      (str_store_troop_name_by_count, s2, ":upgrade1", "$upgrade_count"),

      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade1", "$g_encountered_party"),
      (val_mul, reg0, "$upgrade_count"),

      (store_troop_gold, ":gold", "trp_player"),
      (ge, ":gold", reg0),
    ],
    "Promote all {s1} to {s2}{reg0? ({reg0} denars):}",
    [
      (troop_get_slot, ":upgrade1", "$g_upgrade_troop", slot_troop_sod_upgrade1),
	  (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade1", "$g_encountered_party"),
      (val_mul, reg0, "$upgrade_count"),
	  (try_begin),
		(gt, reg0, 0),
		(troop_remove_gold, "trp_player", reg0),
	  (try_end),
      (party_remove_members, "p_main_party", "$g_upgrade_troop", "$upgrade_count"),
      (party_add_members, "p_main_party", ":upgrade1", "$upgrade_count"),
      (jump_to_menu, "mnu_sod_upgrade_continue"),
    ]
  ),

  # Upgrade five to upgrade1
  ("marshal_upgrade_choose2",
    [
      (eq, "$can_upgrade1", 1),
      (ge, "$upgrade_count", 5),

      (troop_get_slot, ":upgrade1", "$g_upgrade_troop", slot_troop_sod_upgrade1),

      (str_store_troop_name_by_count, s1, "$g_upgrade_troop", "$upgrade_count"),
      (str_store_troop_name_by_count, s2, ":upgrade1", "$upgrade_count"),

      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade1", "$g_encountered_party"),
      (val_mul, reg0, 5),

      (store_troop_gold, ":gold", "trp_player"),
      (ge, ":gold", reg0),
    ],
    "Promote five {s1} to {s2}{reg0? ({reg0} denars):}",
    [
      (troop_get_slot, ":upgrade1", "$g_upgrade_troop", slot_troop_sod_upgrade1),
      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade1", "$g_encountered_party"),
      (val_mul, reg0, 5),
	  (try_begin),
		(gt, reg0, 0),
		(troop_remove_gold, "trp_player", reg0),
	  (try_end),
      (party_remove_members, "p_main_party", "$g_upgrade_troop", 5),
      (party_add_members, "p_main_party", ":upgrade1", 5),
      (jump_to_menu, "mnu_sod_upgrade_continue"),
    ]
  ),

  # Upgrade one to upgrade1
  ("marshal_upgrade_choose3",
    [
      (eq, "$can_upgrade1", 1),
      (ge, "$upgrade_count", 1),

      (troop_get_slot, ":upgrade1", "$g_upgrade_troop", slot_troop_sod_upgrade1),

      (str_store_troop_name, s1, "$g_upgrade_troop"),
      (str_store_troop_name, s2, ":upgrade1"),

      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade1", "$g_encountered_party"),

      (store_troop_gold, ":gold", "trp_player"),
      (ge, ":gold", reg0),
    ],
    "Promote one {s1} to {s2}{reg0? ({reg0} denars):}",
    [
      (troop_get_slot, ":upgrade1", "$g_upgrade_troop", slot_troop_sod_upgrade1),
      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade1", "$g_encountered_party"),
	  (try_begin),
		(gt, reg0, 0),
		(troop_remove_gold, "trp_player", reg0),
	  (try_end),
      (party_remove_members, "p_main_party", "$g_upgrade_troop", 1),
      (party_add_members, "p_main_party", ":upgrade1", 1),
      (jump_to_menu, "mnu_sod_upgrade_continue"),
    ]
  ),

  # Upgrade all to upgrade2
  ("marshal_upgrade_choose4",
    [
      (eq, "$can_upgrade2", 1),
      (gt, "$upgrade_count", 1),
      (neq, "$upgrade_count", 5),

      (troop_get_slot, ":upgrade2", "$g_upgrade_troop", slot_troop_sod_upgrade2),

      (str_store_troop_name_by_count, s1, "$g_upgrade_troop", "$upgrade_count"),
      (str_store_troop_name_by_count, s2, ":upgrade2", "$upgrade_count"),

      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade2", "$g_encountered_party"),
      (val_mul, reg0, "$upgrade_count"),

      (store_troop_gold, ":gold", "trp_player"),
      (ge, ":gold", reg0),
    ],
    "Promote all {s1} to {s2}{reg0? ({reg0} denars):}",
    [
      (troop_get_slot, ":upgrade2", "$g_upgrade_troop", slot_troop_sod_upgrade2),
      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade2", "$g_encountered_party"),
      (val_mul, reg0, "$upgrade_count"),
	  (try_begin),
		(gt, reg0, 0),
		(troop_remove_gold, "trp_player", reg0),
	  (try_end),
      (party_remove_members, "p_main_party", "$g_upgrade_troop", "$upgrade_count"),
      (party_add_members, "p_main_party", ":upgrade2", "$upgrade_count"),
      (jump_to_menu, "mnu_sod_upgrade_continue"),
    ]
  ),

  # Upgrade five to upgrade2
  ("marshal_upgrade_choose5",
    [
      (eq, "$can_upgrade2", 1),
      (ge, "$upgrade_count", 5),

      (troop_get_slot, ":upgrade2", "$g_upgrade_troop", slot_troop_sod_upgrade2),

      (str_store_troop_name_by_count, s1, "$g_upgrade_troop", "$upgrade_count"),
      (str_store_troop_name_by_count, s2, ":upgrade2", "$upgrade_count"),

      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade2", "$g_encountered_party"),
      (val_mul, reg0, 5),

      (store_troop_gold, ":gold", "trp_player"),
      (ge, ":gold", reg0),
    ],
    "Promote five {s1} to {s2}{reg0? ({reg0} denars):}",
    [
      (troop_get_slot, ":upgrade2", "$g_upgrade_troop", slot_troop_sod_upgrade2),
      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade2", "$g_encountered_party"),
      (val_mul, reg0, 5),
	  (try_begin),
		(gt, reg0, 0),
		(troop_remove_gold, "trp_player", reg0),
	  (try_end),
      (party_remove_members, "p_main_party", "$g_upgrade_troop", 5),
      (party_add_members, "p_main_party", ":upgrade2", 5),
      (jump_to_menu, "mnu_sod_upgrade_continue"),
    ]
  ),

  # Upgrade one to upgrade2
  ("marshal_upgrade_choose6",
    [
      (eq, "$can_upgrade2", 1),
      (ge, "$upgrade_count", 1),

      (troop_get_slot, ":upgrade2", "$g_upgrade_troop", slot_troop_sod_upgrade2),

      (str_store_troop_name, s1, "$g_upgrade_troop"),
      (str_store_troop_name, s2, ":upgrade2"),

      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade2", "$g_encountered_party"),

      (store_troop_gold, ":gold", "trp_player"),
      (ge, ":gold", reg0),
    ],
    "Promote one {s1} to {s2}{reg0? ({reg0} denars):}",
    [
      (troop_get_slot, ":upgrade2", "$g_upgrade_troop", slot_troop_sod_upgrade2),
      (call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade2", "$g_encountered_party"),
	  (try_begin),
		(gt, reg0, 0),
		(troop_remove_gold, "trp_player", reg0),
	  (try_end),
      (party_remove_members, "p_main_party", "$g_upgrade_troop", 1),
      (party_add_members, "p_main_party", ":upgrade2", 1),
      (jump_to_menu, "mnu_sod_upgrade_continue"),
    ]
  ),
  ("return",[],"Return.",[(jump_to_menu, "$jump_menu"),])
	]),
]
