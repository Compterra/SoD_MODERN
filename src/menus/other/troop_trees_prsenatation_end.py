MENUS = [
("troop_trees_prsenatation_end", 0,
	"Cassian Varro closes the campaign ledger.",
	"none", [
	(try_begin),
		(eq, "$g_sod_sa_in_court", 0),
		(start_map_conversation, "trp_sod_strategy_advisor"),
		(change_screen_return),
	(else_try),
		(call_script, "script_enter_court", "$g_encountered_party"),
		(change_screen_map_conversation, "trp_sod_strategy_advisor"),
	(try_end),
	],
	[],),
]
