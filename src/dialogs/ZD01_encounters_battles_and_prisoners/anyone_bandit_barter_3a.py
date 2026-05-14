DIALOGS = [
[anyone, "bandit_barter_3a", [], "There. Coin weighs less than blood. Ride on before someone changes the price.", "close_window", [
    (store_current_hours, ":protected_until"),
    (val_add, ":protected_until", 72),
    (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, ":protected_until"),
    (party_ignore_player, "$g_encountered_party", 72),
    (call_script, "script_sod_note_hostile_reputation", 7),
    (call_script, "script_sod_note_hostile_reputation", 7),
    (assign, "$g_leave_encounter", 1)
    ]],
]
