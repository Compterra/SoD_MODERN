DIALOGS = [
[anyone|plyr, "castle_patrol_talk", [
    (store_troop_gold, ":gold", "trp_player"),
    (ge, ":gold", 200),
    (party_get_slot, ":quality", "$g_encountered_party", slot_party_sod_patrol_quality),
    (lt, ":quality", 40),
], "Two hundred denars buys discretion. You saw a lawful traveler, nothing more.", "close_window", [
    (call_script, "script_sod_player_charge_gold", 200),
    (store_current_hours, ":protected_until"),
    (val_add, ":protected_until", 48),
    (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, ":protected_until"),
    (party_ignore_player, "$g_encountered_party", 48),
    (assign, "$g_leave_encounter", 1),
]],
]
