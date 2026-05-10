DIALOGS = [
[anyone, "deserter_honor_appeal", [
    (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
    (ge, ":persuasion", 2),
    (party_get_num_companions, ":player_size", "p_main_party"),
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (store_mul, ":needed_size", ":enemy_size", 2),
    (this_or_next|ge, ":player_size", ":needed_size"),
    (ge, "$player_honor", 30),
], "Maybe there is still a road back from this. We will not test your mercy today.", "close_window", [
    (call_script, "script_sod_note_hostile_reputation", 1),
    (call_script, "script_sod_resolve_hostile_party_noncombat", "$g_encountered_party"),
]],
]
