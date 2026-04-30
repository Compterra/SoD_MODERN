DIALOGS = [
[anyone, "gm_promote",[
	(store_relation, ":rel", "fac_player_supporters_faction", "$g_talk_troop_faction"),
	(ge, ":rel", 10),
	(faction_set_slot, "$g_talk_troop_faction", slot_faction_upgrade_permission, 1),
	], "You have my permission.", "gm_pretalk",[]],
]
