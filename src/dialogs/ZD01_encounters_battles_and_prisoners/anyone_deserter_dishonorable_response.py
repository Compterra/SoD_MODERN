DIALOGS = [
[anyone, "deserter_dishonorable_response", [], "Aye. We heard. Better to die armed than kneel to a butcher.", "close_window", [
    (assign, "$g_enemy_party", "$g_encountered_party"),
    (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
    (encounter_attack),
]],
]
