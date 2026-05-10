DIALOGS = [
[trp_sod_strategy_advisor|auto_proceed, "event_triggered", [
	(eq, "$g_sod_player_asked_for_troop_tree", 1),
	(this_or_next|main_party_has_troop, "trp_sod_strategy_advisor"),
	(eq, "$g_sod_sa_in_court", 1),
	(assign, "$g_sod_player_asked_for_troop_tree", 0),
	], "-welcome_text-", "sa_select_3", []],
]
