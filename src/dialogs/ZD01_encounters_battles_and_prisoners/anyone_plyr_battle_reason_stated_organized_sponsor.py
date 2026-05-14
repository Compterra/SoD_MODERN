DIALOGS = [
[anyone|plyr, "battle_reason_stated", [
    (gt, "$g_encountered_party", 0),
    (party_is_active, "$g_encountered_party"),
    (party_get_template_id, ":template", "$g_encountered_party"),
    (this_or_next|eq, ":template", "pt_elephant_guard_ravaging_bandits"),
    (this_or_next|eq, ":template", "pt_conquistadors_ravaging_bandits"),
    (this_or_next|eq, ":template", "pt_serpent_host_ravaging_bandits"),
    (eq, ":template", "pt_black_khergit_raiders"),
], "Who put you on this road?", "organized_raider_sponsor_question", []],
]
