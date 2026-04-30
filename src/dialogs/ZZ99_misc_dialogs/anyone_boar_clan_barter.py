DIALOGS = [
[anyone, "boar_clan_barter",
   [], "Silver without blood, that's our favourite kind.", "close_window", [
	(store_current_hours, ":protected_until"),
	(val_add, ":protected_until", 72),
    (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, ":protected_until"),
    (party_ignore_player, "$g_encountered_party", 72),
	(assign, "$g_leave_encounter", 1),
   ]],
]
