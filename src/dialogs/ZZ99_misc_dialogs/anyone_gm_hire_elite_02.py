DIALOGS = [
[anyone,"gm_hire_elite", [
	(assign, ":enable", 0),
	(call_script, "script_merc_get_elite_relation_requirement", "$g_talk_troop_faction"),
	(assign, ":required_relation", reg0),
	(try_begin),
		(faction_get_slot, ":mercenaries", "fac_player_faction", slot_faction_merc_pact),
		(this_or_next|eq, ":mercenaries", "$g_talk_troop_faction"),
		(ge, "$g_talk_troop_faction_relation", ":required_relation"),
		(assign, ":enable", 1),
	(else_try),
		(this_or_next|eq, "$g_talk_troop", slavers_guild_master),
		(eq, "$g_talk_troop", slavers_rep),
		(ge, "$g_talk_troop_faction_relation", ":required_relation"),
		(assign, ":enable", 1),
	(try_end),
	(eq, ":enable", 1),
  ], "These soldiers are the cream of the crop of our army, and your standing is high enough that we will trust them to you.", "gm_pretalk",[(set_mercenary_source_party,"$gm_party_elite"),[change_screen_buy_mercenaries]]],
]
