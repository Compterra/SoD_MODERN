DIALOGS = [
[anyone, "bandit_intimidate", [
    (party_get_num_companions, ":player_size", "p_main_party"),
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (store_mul, ":needed_size", ":enemy_size", 3),
    (ge, ":player_size", ":needed_size"),
], "Aye. We counted. There are softer roads and poorer memories elsewhere.", "close_window", [
    (call_script, "script_sod_note_hostile_reputation", 5),
    (call_script, "script_sod_resolve_hostile_party_noncombat", "$g_encountered_party"),
]],
]
