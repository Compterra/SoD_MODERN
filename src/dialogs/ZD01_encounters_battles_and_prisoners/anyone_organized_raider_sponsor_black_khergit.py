DIALOGS = [
[anyone, "organized_raider_sponsor_question", [
    (gt, "$g_encountered_party", 0),
    (party_is_active, "$g_encountered_party"),
    (party_get_template_id, ":template", "$g_encountered_party"),
    (eq, ":template", "pt_black_khergit_raiders"),
], "The Khan's shadow rides ahead of us. If you can see us, the answer is already too close.", "battle_reason_stated", []],
]
