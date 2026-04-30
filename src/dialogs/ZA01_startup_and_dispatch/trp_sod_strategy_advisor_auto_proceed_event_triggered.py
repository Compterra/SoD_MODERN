DIALOGS = [
[trp_sod_strategy_advisor|auto_proceed, "event_triggered", [
	(eq, "$g_sod_player_asked_for_troop_tree", 1),
	(assign, "$g_sod_player_asked_for_troop_tree", 0),
	], "-welcome_text-", "sa_select_3", []],
]
