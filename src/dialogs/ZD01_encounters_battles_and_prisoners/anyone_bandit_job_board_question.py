DIALOGS = [
[anyone, "sod_bandit_job_board_question", [
    (party_get_slot, ":origin_center", "$g_encountered_party", slot_party_sod_threat_sponsor_center),
    (str_store_party_name, s6, ":origin_center"),
], "Sent? No. We smelled weak patrols around {s6}, and your board put a price on being noticed.", "bandit_talk", []],
]
