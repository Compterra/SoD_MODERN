DIALOGS = [
[anyone, "sod_job_board_timing_line", [
    (call_script, "script_sod_hostile_encounter_profile", "$g_encountered_party"),
    (eq, reg25, 1),
], "Because fear ripens. {s10} has days left to imagine us at every gate and ford.", "battle_reason_stated", []],
]
