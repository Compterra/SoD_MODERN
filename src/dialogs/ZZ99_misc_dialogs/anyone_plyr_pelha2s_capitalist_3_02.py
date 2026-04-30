DIALOGS = [
[anyone|plyr, "pelha2s_capitalist_3", [
	(store_troop_gold, ":gold", "trp_player"),
	(ge, ":gold", 3000),
	], "Always the businessman I see. Very well, I'll pay. See you around.", "close_window", [
	(troop_remove_gold, "trp_player", 3000),
	(assign, "$g_player_surrenders", 0),
	(store_current_hours, ":protected_until"),
    (val_add, ":protected_until", 72),
    (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, ":protected_until"),
    (party_ignore_player, "$g_encountered_party", 72),
    (assign, "$g_leave_encounter", 1)
	] ],
]
