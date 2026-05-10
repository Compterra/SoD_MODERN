DIALOGS = [
[anyone|plyr, "battle_reason_stated", [
    (call_script, "script_sod_hostile_encounter_profile", "$g_encountered_party"),
    (eq, reg22, 1),
], "The board names you. Surrender, and this ends before more men die.", "sod_job_board_surrender_demand", []],
]
