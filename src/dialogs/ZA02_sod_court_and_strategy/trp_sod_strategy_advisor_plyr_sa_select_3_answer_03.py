DIALOGS = [
[trp_sod_strategy_advisor|plyr, "sa_select_3_answer", [], "Lay out their divisions and ranks as a proper order of battle.", "close_window", [
	(assign, "$g_sod_player_asked_for_troop_tree", 1),
	(finish_mission),
	(jump_to_menu, "mnu_troop_trees_prsenatation"),
	]],
]
