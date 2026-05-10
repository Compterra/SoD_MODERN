DIALOGS = [
[anyone, "bandit_barter", [
    (this_or_next|ge, "$g_sod_hostile_shakedown_count", 3),
    (eq, "$g_sod_nemesis_reason", sod_nemesis_reason_robbed),
    (ge, "$g_sod_nemesis_state", sod_nemesis_state_watching),
], "No. We heard about you turning robbers into taxpayers. This time, steel speaks before silver.", "close_window", [
    (encounter_attack),
]],
]
