DIALOGS = [
[anyone, "special_raider_war_aims", [
    (gt, "$g_encountered_party", 0),
    (party_is_active, "$g_encountered_party"),
    (party_get_template_id, ":template", "$g_encountered_party"),
    (eq, ":template", "pt_elephant_guard_ravaging_bandits"),
], "The war of giants. We break roads first, then armies, then the memory of both.", "battle_reason_stated", []],
]
