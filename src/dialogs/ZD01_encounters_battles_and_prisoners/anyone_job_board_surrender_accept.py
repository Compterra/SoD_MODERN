DIALOGS = [
[anyone, "sod_job_board_surrender_demand", [
    (call_script, "script_sod_hostile_encounter_profile", "$g_encountered_party"),
    (eq, reg22, 1),
    (eq, reg23, 1),
], "Enough. {s10} bought a stronger hand than ours. We yield the road.", "close_window", [
    (call_script, "script_sod_note_hostile_reputation", 3),
    (call_script, "script_sod_resolve_hostile_party_noncombat", "$g_encountered_party"),
]],
]
