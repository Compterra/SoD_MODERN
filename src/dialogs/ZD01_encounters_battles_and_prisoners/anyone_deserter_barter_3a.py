DIALOGS = [
[anyone, "deserter_barter_3a", [], "Heh. That wasn't difficult now was it? All right. Go now.", "close_window", [
    (store_current_hours, ":protected_until"),
    (val_add, ":protected_until", 72),
    (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, ":protected_until"),
    (party_ignore_player, "$g_encountered_party", 72),

    (assign, "$g_leave_encounter", 1)
    ]],
]
