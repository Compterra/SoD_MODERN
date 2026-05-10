DIALOGS = [
[anyone|plyr, "slaver_world_caravan_talk",
  [
    (main_party_has_troop, "trp_npc7"),
    (call_script, "script_cf_sod_companion_campaign_available", "trp_npc7", sod_companion_campaign_mode_travel),
    (eq, "$g_sod_deshavi_trail_warning_pending", 1),
    (eq, "$g_sod_deshavi_trail_warning_cause", 2),
    (eq, "$g_sod_deshavi_trail_witnessed", 0),
    (eq, "$g_sod_deshavi_trail_confronted", 0),
    (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Deshavi found rope marks and hunter tracks. Were those yours?", "slaver_world_caravan_companion_deshavi_pursuer", []],
]
