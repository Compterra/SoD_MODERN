DIALOGS = [
[anyone, "bandit_outlaw_slayer_reaction", [
    (party_get_num_companions, ":player_size", "p_main_party"),
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (ge, ":player_size", ":enemy_size"),
], "We know your work. Not today. Not us.", "close_window", [
    (call_script, "script_sod_note_hostile_reputation", 5),
    (call_script, "script_sod_resolve_hostile_party_noncombat", "$g_encountered_party"),
]],
]
