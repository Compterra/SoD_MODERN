DIALOGS = [
[trp_sod_strategy_advisor|plyr, "sod_sa_last_order_choice", [], "Expose the network publicly. Let the realm know what was done in secret.", "sod_sa_last_order_after_expose", [
    (call_script, "script_sod_strategy_advisor_resolve_last_order", sod_mentor_last_order_exposed),
]],
]
