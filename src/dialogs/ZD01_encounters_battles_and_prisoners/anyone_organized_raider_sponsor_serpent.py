DIALOGS = [
[anyone, "organized_raider_sponsor_question", [
    (gt, "$g_encountered_party", 0),
    (party_is_active, "$g_encountered_party"),
    (party_get_template_id, ":template", "$g_encountered_party"),
    (eq, ":template", "pt_serpent_host_ravaging_bandits"),
], "The Serpent does not send. It coils, and we move where the pressure tightens.", "battle_reason_stated", []],
]
