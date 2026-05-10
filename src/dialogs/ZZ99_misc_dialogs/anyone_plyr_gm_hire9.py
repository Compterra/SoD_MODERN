DIALOGS = [
[anyone|plyr, "gm_hire9", [
					(assign, reg19, "$merc_cost"),
					(store_troop_gold, ":gold", "trp_player"),
					(ge, ":gold", reg19),
					(eq, "$g_sod_merc_player_hire_blocked", 0),
    ],"All right. Here is the {reg19} denar retainer.", "gm_hire10", [
		(call_script, "script_sod_player_charge_gold", "$merc_cost"),]],
]
