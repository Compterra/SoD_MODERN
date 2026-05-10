DIALOGS = [
[anyone, "bandit_scatter_demand", [], "No prize is worth this. Scatter!", "close_window", [
    (call_script, "script_sod_note_hostile_reputation", 5),
    (call_script, "script_sod_resolve_hostile_party_noncombat", "$g_encountered_party"),
    (display_message, "@The raiders break formation and flee in every direction."),
]],
]
