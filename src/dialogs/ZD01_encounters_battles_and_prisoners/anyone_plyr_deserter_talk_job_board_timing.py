DIALOGS = [
[anyone|plyr, "deserter_talk", [
    (call_script, "script_sod_hostile_encounter_profile", "$g_encountered_party"),
    (eq, reg22, 1),
], "The contract still has time. Why stay where hunters can find you?", "sod_job_board_timing_line", []],
]
