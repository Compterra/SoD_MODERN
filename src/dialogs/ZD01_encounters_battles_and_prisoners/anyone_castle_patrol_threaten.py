DIALOGS = [
[anyone, "castle_patrol_threaten", [
    (party_get_num_companions, ":patrol_size", "$g_encountered_party"),
    (party_get_num_companions, ":player_size", "p_main_party"),
    (ge, ":player_size", ":patrol_size"),
], "We know it. We will mark your passage as disputed and keep our dead out of the ditch.", "close_window", [
    (store_current_hours, ":protected_until"),
    (val_add, ":protected_until", 24),
    (party_set_slot, "$g_encountered_party", slot_party_ignore_player_until, ":protected_until"),
    (party_ignore_player, "$g_encountered_party", 24),
    (assign, "$g_leave_encounter", 1),
]],
[anyone, "castle_patrol_threaten", [], "A famous banner still bleeds, and contraband hides under fine cloth as easily as rags. Try us if you must.", "castle_patrol_talk", []],
]
