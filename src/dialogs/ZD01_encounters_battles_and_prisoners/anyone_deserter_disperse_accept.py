DIALOGS = [
[anyone, "deserter_disperse_demand", [
    (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
    (party_get_num_companions, ":player_size", "p_main_party"),
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (store_mul, ":overwhelming_size", ":enemy_size", 3),
    (this_or_next|ge, ":player_size", ":overwhelming_size"),
    (ge, ":persuasion", 3),
], "Done. We split here. No banner, no captain, no road brothers.", "close_window", [
    (call_script, "script_sod_note_hostile_reputation", 1),
    (call_script, "script_sod_resolve_hostile_party_noncombat", "$g_encountered_party"),
    (display_message, "@The deserter band breaks apart and vanishes from the roads."),
]],
]
