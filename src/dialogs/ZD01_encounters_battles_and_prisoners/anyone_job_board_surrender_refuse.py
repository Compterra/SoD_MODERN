DIALOGS = [
[anyone, "sod_job_board_surrender_demand", [
    (call_script, "script_sod_hostile_encounter_profile", "$g_encountered_party"),
    (eq, reg22, 1),
], "The board can write what it likes. {s10} still has to pay in blood before it buys our fear.", "close_window", [
    (assign, "$g_enemy_party", "$g_encountered_party"),
    (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
    (encounter_attack),
]],
]
