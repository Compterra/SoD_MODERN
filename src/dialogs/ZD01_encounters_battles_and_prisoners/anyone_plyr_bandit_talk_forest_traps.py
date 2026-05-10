DIALOGS = [
[anyone|plyr, "bandit_talk", [
    (party_get_template_id, ":template", "$g_encountered_party"),
    (eq, ":template", "pt_forest_bandits"),
], "If you wanted an ambush, you should have stayed hidden.", "forest_bandit_traps", []],
]
