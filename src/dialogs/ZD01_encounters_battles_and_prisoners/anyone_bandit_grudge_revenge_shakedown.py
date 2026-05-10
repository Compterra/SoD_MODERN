DIALOGS = [
[anyone, "bandit_talk", [
    (this_or_next|ge, "$g_sod_hostile_shakedown_count", 3),
    (eq, "$g_sod_nemesis_reason", sod_nemesis_reason_robbed),
    (ge, "$g_sod_nemesis_state", sod_nemesis_state_hunting),
    (store_random_in_range, ":revenge_roll", 0, 100),
    (lt, ":revenge_roll", 35),
], "You are the one making outlaws pay tolls. No bargain today. The roads need to see you bleed.", "close_window", [
    (encounter_attack),
]],
]
