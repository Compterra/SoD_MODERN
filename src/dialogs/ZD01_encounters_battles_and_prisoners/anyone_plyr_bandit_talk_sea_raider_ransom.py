DIALOGS = [
[anyone|plyr, "bandit_talk", [
    (party_get_template_id, ":template", "$g_encountered_party"),
    (eq, ":template", "pt_sea_raiders"),
], "What ransom does a beach thief imagine I am worth?", "sea_raider_ransom_mock", []],
]
