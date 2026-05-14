DIALOGS = [
[anyone, "organized_raider_sponsor_question", [
    (gt, "$g_encountered_party", 0),
    (party_is_active, "$g_encountered_party"),
    (party_get_template_id, ":template", "$g_encountered_party"),
    (eq, ":template", "pt_elephant_guard_ravaging_bandits"),
], "No petty lord. We march where the giants' oath points, and your road lies beneath it.", "battle_reason_stated", []],
]
