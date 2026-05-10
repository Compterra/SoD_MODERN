DIALOGS = [
[anyone|plyr, "bandit_talk", [
    (party_get_template_id, ":template", "$g_encountered_party"),
    (eq, ":template", "pt_mountain_bandits"),
], "Name your mountain toll, then.", "mountain_bandit_toll", []],
]
