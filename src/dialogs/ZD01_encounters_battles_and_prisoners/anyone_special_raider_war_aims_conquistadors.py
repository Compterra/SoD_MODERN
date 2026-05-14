DIALOGS = [
[anyone, "special_raider_war_aims", [
    (gt, "$g_encountered_party", 0),
    (party_is_active, "$g_encountered_party"),
    (party_get_template_id, ":template", "$g_encountered_party"),
    (eq, ":template", "pt_conquistadors_ravaging_bandits"),
], "A war for claims not yet written on your maps. Your purse is merely the first province.", "battle_reason_stated", []],
]
