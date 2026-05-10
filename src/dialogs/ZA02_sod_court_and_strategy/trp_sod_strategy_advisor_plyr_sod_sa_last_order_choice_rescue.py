DIALOGS = [
[trp_sod_strategy_advisor|plyr, "sod_sa_last_order_choice", [], "Use the network to extract refugees, informants, and families left behind.", "sod_sa_last_order_after_rescue", [
    (call_script, "script_sod_strategy_advisor_resolve_last_order", sod_mentor_last_order_rescue),
]],
]
