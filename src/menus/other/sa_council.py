MENUS = [
("sa_council", 0,
	"One of Your companions, Yor Strategy Advisor, comes to your tent after the battle asking for private audience. - My Liege - he begins - I never asked you anything and served you faithfuly. I'm old and tired. I cannot fight as well as in the good old days under Your father's command. Thus I ask You my Liege for permission join Your court and serve You with my administration skills.",
	"none", [
	],
	[
	("accept",[],"You have my premission, this castle is now your home. (+50 demesne and propaganda points)",[
	(assign, "$g_sod_sa_in_court", 1),
	(party_remove_members, "p_main_party", "trp_sod_strategy_advisor", 1),
	(troop_clear_inventory, "trp_sod_strategy_advisor"),
	(troop_add_item, "trp_sod_strategy_advisor", "itm_dynasty_outfit", 0),
	(troop_add_item, "trp_sod_strategy_advisor", "itm_elephant_guard_gloves", 0),
	(troop_add_item, "trp_sod_strategy_advisor", "itm_dynasty_oufit_greaves", 0),
	(troop_equip_items, "trp_sod_strategy_advisor"),
	(change_screen_return),
	]),
	("deny",[],"I need you in my travels. You're staying with me.",[
	(call_script, "script_change_player_honor", -10),
	(change_screen_return),
	]),
	]),
]
