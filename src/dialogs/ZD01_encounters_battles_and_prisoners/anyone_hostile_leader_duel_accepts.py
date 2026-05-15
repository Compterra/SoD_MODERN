DIALOGS = [
[anyone, "hostile_leader_duel_challenge", [], "A pretty speech. But I brought a company, not a theatre. Kill them all!", "close_window", [
    (assign, "$g_enemy_party", "$g_encountered_party"),
    (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
    (encounter_attack),
]],
]
