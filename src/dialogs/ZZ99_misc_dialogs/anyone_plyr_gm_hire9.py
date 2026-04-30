DIALOGS = [
[anyone|plyr, "gm_hire9", [
					(assign, reg19, "$merc_cost"),
					(store_troop_gold, ":gold", "trp_player"),
					(ge, ":gold", reg19),
    ],"All right. Here is {reg19} denars.", "gm_hire10", [
		(troop_remove_gold, "trp_player", "$merc_cost"),]],
]
