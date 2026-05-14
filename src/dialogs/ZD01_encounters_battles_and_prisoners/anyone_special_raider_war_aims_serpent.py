DIALOGS = [
[anyone, "special_raider_war_aims", [
    (gt, "$g_encountered_party", 0),
    (party_is_active, "$g_encountered_party"),
    (party_get_template_id, ":template", "$g_encountered_party"),
    (eq, ":template", "pt_serpent_host_ravaging_bandits"),
], "The Serpent coils where kingdoms grow fat. We are hunger given banners.", "battle_reason_stated", []],
]
