DIALOGS = [
[anyone, "organized_raider_sponsor_question", [
    (gt, "$g_encountered_party", 0),
    (party_is_active, "$g_encountered_party"),
    (party_get_template_id, ":template", "$g_encountered_party"),
    (eq, ":template", "pt_conquistadors_ravaging_bandits"),
], "Captains, charters, hungry crowns across the water. Pick one. They all spend men the same way.", "battle_reason_stated", []],
]
