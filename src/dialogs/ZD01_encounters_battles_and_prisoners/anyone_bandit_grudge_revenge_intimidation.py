DIALOGS = [
[anyone, "bandit_talk", [
    (this_or_next|ge, "$g_sod_hostile_intimidation_count", 5),
    (eq, "$g_sod_nemesis_reason", sod_nemesis_reason_humiliation),
    (ge, "$g_sod_nemesis_state", sod_nemesis_state_hunting),
    (store_random_in_range, ":revenge_roll", 0, 100),
    (lt, ":revenge_roll", 35),
], "Too many crews ran from your banner. We kill you, or we never hear the end of it.", "close_window", [
    (encounter_attack),
]],
]
