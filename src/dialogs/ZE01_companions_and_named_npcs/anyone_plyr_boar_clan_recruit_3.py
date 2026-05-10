DIALOGS = [
[anyone|plyr, "boar_clan_recruit_3", [
	(assign, reg5, "$g_sod_boar_hire_cost"),
	(val_clamp, reg5, 1, 20001),
	(assign, "$g_sod_boar_hire_cost", reg5),
	(store_troop_gold, ":gold", "trp_player"),
	(ge, ":gold", reg5),
	], "Here, {reg5} denars.", "close_window", [
	(assign, reg5, "$g_sod_boar_hire_cost"),
	(val_clamp, reg5, 1, 20001),
	(assign, "$g_sod_boar_hire_cost", reg5),
	(assign, ":hire_cost", reg5),
	(call_script, "script_sod_player_charge_gold", reg5),
	(call_script, "script_sod_boar_clan_convert_to_player_mercenaries"),
	(call_script, "script_sod_boar_clan_apply_player_action", sod_boar_action_hire_band, ":hire_cost"),
	(assign, "$g_sod_boar_hire_cost", 0),
	(call_script, "script_change_player_relation_with_faction", "fac_sod_merc_guild7", 5),
	]],
]
