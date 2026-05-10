DIALOGS = [
[anyone|plyr, "tavernkeeper_talk",
    [
        (main_party_has_troop, "trp_npc1"),
        (call_script, "script_cf_sod_companion_campaign_available", "trp_npc1", sod_companion_campaign_mode_dialog),
        (eq, "$g_sod_borcha_road_pending", 1),
        (eq, "$g_sod_borcha_road_witnessed", 0),
        (eq, "$current_town", "$g_sod_borcha_road_origin_center"),
        (troop_slot_eq, "trp_npc1", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
    ],
    "Borcha says the side road from here has been swept too clean. Who came through last?", "tavernkeeper_companion_borcha_road", []],
]
