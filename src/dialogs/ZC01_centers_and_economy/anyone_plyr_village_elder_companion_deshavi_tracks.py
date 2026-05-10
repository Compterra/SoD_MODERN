DIALOGS = [
[anyone|plyr, "village_elder_talk",
  [
    (main_party_has_troop, "trp_npc7"),
    (call_script, "script_cf_sod_companion_campaign_available", "trp_npc7", sod_companion_campaign_mode_scene),
    (eq, "$g_sod_deshavi_trail_warning_pending", 1),
    (eq, "$current_town", "$g_sod_deshavi_trail_focus_center"),
    (eq, "$g_sod_deshavi_trail_confronted", 0),
    (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Deshavi followed signs here. Who passed this way?", "village_elder_companion_deshavi_tracks",
  []],
]
