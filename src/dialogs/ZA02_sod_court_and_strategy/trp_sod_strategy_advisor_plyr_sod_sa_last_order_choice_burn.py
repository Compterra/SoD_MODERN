DIALOGS = [
[trp_sod_strategy_advisor|plyr, "sod_sa_last_order_choice", [], "Burn the network. Protect those who served in secret.", "sod_sa_last_order_after_burn", [
    (call_script, "script_sod_strategy_advisor_resolve_last_order", sod_mentor_last_order_burned),
]],
]
