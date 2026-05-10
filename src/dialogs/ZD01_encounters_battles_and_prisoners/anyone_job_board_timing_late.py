DIALOGS = [
[anyone, "sod_job_board_timing_line", [
    (call_script, "script_sod_hostile_encounter_profile", "$g_encountered_party"),
    (eq, reg25, -1),
], "Almost too late, hunter. {s10} must be counting candles and pretending your delay was strategy.", "battle_reason_stated", []],
]
