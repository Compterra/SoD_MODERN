DIALOGS = [
[anyone|plyr, "tavernkeeper_talk",
    [
        (main_party_has_troop, "trp_npc16"),
        (call_script, "script_cf_sod_companion_campaign_available", "trp_npc16", sod_companion_campaign_mode_dialog),
        (eq, "$g_sod_klethi_old_job_pending", 1),
        (eq, "$g_sod_klethi_old_job_contacted", 0),
        (eq, "$current_town", "$g_sod_klethi_old_job_focus_center"),
        (troop_slot_eq, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
    ],
    "A friend of mine saw an old mark here. Who has been asking after Klethi?", "tavernkeeper_companion_klethi_contact", []],
]
