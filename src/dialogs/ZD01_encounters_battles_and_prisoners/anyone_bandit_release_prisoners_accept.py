DIALOGS = [
[anyone, "bandit_release_prisoners_demand", [
    (party_get_num_prisoners, ":prisoners", "$g_encountered_party"),
    (gt, ":prisoners", 0),
    (party_get_num_companions, ":player_size", "p_main_party"),
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (store_mul, ":needed_size", ":enemy_size", 2),
    (ge, ":player_size", ":needed_size"),
    (party_get_free_prisoners_capacity, ":free_capacity", "p_main_party"),
    (gt, ":free_capacity", 0),
], "Take them. Prisoners slow the feet anyway.", "close_window", [
    (call_script, "script_sod_transfer_hostile_prisoners_to_player", "$g_encountered_party"),
    (assign, reg6, reg0),
    (call_script, "script_sod_note_hostile_reputation", 1),
    (call_script, "script_sod_resolve_hostile_party_noncombat", "$g_encountered_party"),
    (display_message, "@The bandits release {reg6} prisoners into your custody before fleeing."),
]],
]
