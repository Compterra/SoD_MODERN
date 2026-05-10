DIALOGS = [
[trp_sod_strategy_advisor|plyr, "startegy_advisor_continue", [
    (quest_slot_eq, "qst_companion_cassian_last_order", slot_quest_sod_runtime_state, sod_quest_state_inactive),
    (store_current_day, ":today"),
    (store_sub, ":days_left", "$g_sod_invasion_begin", ":today"),
    (this_or_next|eq, "$g_sod_sa_in_court", 1),
    (le, ":days_left", 75),
], "The Last Order. What did my father leave you?", "sod_sa_last_order_opening", []],
]
