DIALOGS = [
[anyone, "sod_job_board_surrender_demand", [
    (call_script, "script_sod_hostile_encounter_profile", "$g_encountered_party"),
    (eq, reg22, 1),
], "The board can write what it likes. {s10} still has to pay in blood before it buys our fear.", "close_window", [
    (encounter_attack),
]],
]
