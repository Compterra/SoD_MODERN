DIALOGS = [
[trp_sod_strategy_advisor, "sod_sa_after_6", [], "Cassian Varro. I have not heard it spoken as command in years. I will take a chair in your hall, my liege, but leave a blade within reach.", "close_window", [
	(assign, "$g_sod_sa_in_court", 1),
	(assign, "$sa_talk_after_siege", 0),
	(party_remove_members, "p_main_party", "trp_sod_strategy_advisor", 1),
	(troop_clear_inventory, "trp_sod_strategy_advisor"),
	(troop_add_item, "trp_sod_strategy_advisor", "itm_dynasty_outfit", 0),
	(troop_add_item, "trp_sod_strategy_advisor", "itm_elephant_guard_gloves", 0),
	(troop_add_item, "trp_sod_strategy_advisor", "itm_dynasty_oufit_greaves", 0),
	(troop_equip_items, "trp_sod_strategy_advisor"),
	]],
]
