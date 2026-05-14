DIALOGS = [
[anyone, "special_raider_war_aims", [
    (gt, "$g_encountered_party", 0),
    (party_is_active, "$g_encountered_party"),
    (party_get_template_id, ":template", "$g_encountered_party"),
    (eq, ":template", "pt_black_khergit_raiders"),
], "We ride for old debts and new graves. If you need more answer, survive the first charge.", "battle_reason_stated", []],
]
