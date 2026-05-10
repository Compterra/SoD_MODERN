DIALOGS = [
[anyone, "hostile_leader_duel_challenge", [
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (ge, ":renown", 250),
    (party_get_num_companions, ":player_size", "p_main_party"),
    (party_get_num_companions, ":enemy_size", "$g_encountered_party"),
    (ge, ":player_size", ":enemy_size"),
], "No. I know that name, and I know what happens when fools gamble men on pride. We leave.", "close_window", [
    (call_script, "script_sod_note_hostile_reputation", 5),
    (call_script, "script_sod_resolve_hostile_party_noncombat", "$g_encountered_party"),
]],
]
