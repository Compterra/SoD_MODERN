MENUS = [
("sa_council", 0,
	"Cassian Varro asks for a private audience after the battle. The old soldier has blood on his sleeve and a campaign map under one arm. 'My liege,' he says, 'I can still hold a blade, but your realm needs my mind more than my sword. Give me a place in your hall, and I will serve as Cassian Varro, Strategy Advisor.'",
	"none", [
	],
	[
	("accept",[],"Take your place in my hall, Cassian. I need your counsel alive.",[
	(assign, "$g_sod_sa_in_court", 1),
	(assign, "$sa_talk_after_siege", 0),
	(party_remove_members, "p_main_party", "trp_sod_strategy_advisor", 1),
	(troop_clear_inventory, "trp_sod_strategy_advisor"),
	(troop_add_item, "trp_sod_strategy_advisor", "itm_dynasty_outfit", 0),
	(troop_add_item, "trp_sod_strategy_advisor", "itm_elephant_guard_gloves", 0),
	(troop_add_item, "trp_sod_strategy_advisor", "itm_dynasty_oufit_greaves", 0),
	(troop_equip_items, "trp_sod_strategy_advisor"),
	(change_screen_return),
	]),
	("deny",[],"Not yet. I still need you riding with me.",[
	(display_message, "@Cassian accepts the order, though the old wound bends him before he turns away.", 0xCCCC66),
	(change_screen_return),
	]),
	]),
]
