DIALOGS = [
[anyone, "bandit_hideout_clue_demand", [
    (call_script, "script_sod_store_bandit_hideout_clue", "$g_encountered_party"),
], "{s20}", "bandit_talk", [
    (call_script, "script_sod_note_hostile_reputation", 4),
    (display_message, "@The bandits reveal a likely outlaw gathering region: {s19}."),
]],
]
