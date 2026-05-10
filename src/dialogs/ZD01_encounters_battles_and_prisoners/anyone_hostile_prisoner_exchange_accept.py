DIALOGS = [
[anyone, "hostile_prisoner_exchange_offer", [
    (call_script, "script_sod_has_tradeable_hostile_prisoner"),
    (eq, reg0, 1),
], "A warm body with a price on it. Better than promises. Go, before we reconsider.", "close_window", [
    (call_script, "script_sod_trade_prisoner_to_hostile_party", "$g_encountered_party"),
    (store_current_hours, ":protected_until"),
    (val_add, ":protected_until", 72),
    (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, ":protected_until"),
    (party_ignore_player, "$g_encountered_party", 72),
    (call_script, "script_sod_note_hostile_reputation", 7),
    (assign, "$g_leave_encounter", 1),
]],
]
