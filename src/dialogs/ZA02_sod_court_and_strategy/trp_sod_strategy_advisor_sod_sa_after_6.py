DIALOGS = [
[trp_sod_strategy_advisor, "sod_sa_after_6", [], "My King, I will do this for you.  But if the day comes you need another blade, I will be ready.", "close_window", [
	(assign, "$g_sod_sa_in_court", 1),
	(party_remove_members, "p_main_party", "trp_sod_strategy_advisor", 1),
	]],
]
