DIALOGS = [
[anyone|plyr, "town_dweller_talk",
    [
        (party_slot_eq, "$current_town", slot_party_type, spt_village),
        (main_party_has_troop, "trp_npc7"),
        (call_script, "script_cf_sod_companion_campaign_available", "trp_npc7", sod_companion_campaign_mode_scene),
        (eq, "$g_sod_deshavi_trail_warning_pending", 1),
        (eq, "$current_town", "$g_sod_deshavi_trail_focus_center"),
        (eq, "$g_sod_deshavi_trail_witnessed", 0),
        (eq, "$g_sod_deshavi_trail_confronted", 0),
        (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
    ],
    "Deshavi found signs near here. Did you see who passed?", "town_dweller_companion_deshavi_survivor", []],
]
