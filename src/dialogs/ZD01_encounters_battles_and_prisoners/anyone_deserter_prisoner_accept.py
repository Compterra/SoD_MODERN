DIALOGS = [
[anyone, "deserter_prisoner_demand", [
    (party_get_free_prisoners_capacity, ":free_capacity", "p_main_party"),
    (gt, ":free_capacity", 0),
], "Bound is better than buried. We yield.", "close_window", [
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (party_get_free_prisoners_capacity, ":free_capacity", "p_main_party"),
    (val_min, ":enemy_size", ":free_capacity"),
    (party_add_prisoners, "p_main_party", "trp_watchman", ":enemy_size"),
    (call_script, "script_sod_note_hostile_reputation", 3),
    (call_script, "script_sod_resolve_hostile_party_noncombat", "$g_encountered_party"),
    (display_message, "@The smallest deserter band submits and is taken under guard."),
]],
]
