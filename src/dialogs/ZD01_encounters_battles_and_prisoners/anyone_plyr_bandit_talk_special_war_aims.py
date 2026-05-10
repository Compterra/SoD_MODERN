DIALOGS = [
[anyone|plyr, "bandit_talk", [
    (party_get_template_id, ":template", "$g_encountered_party"),
    (this_or_next|eq, ":template", "pt_elephant_guard_ravaging_bandits"),
    (this_or_next|eq, ":template", "pt_conquistadors_ravaging_bandits"),
    (this_or_next|eq, ":template", "pt_serpent_host_ravaging_bandits"),
    (eq, ":template", "pt_black_khergit_raiders"),
], "Whose war are you fighting out here?", "special_raider_war_aims", []],
]
