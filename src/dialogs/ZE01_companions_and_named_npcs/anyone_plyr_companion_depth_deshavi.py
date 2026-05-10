DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc7"),
    (main_party_has_troop, "trp_npc7"),
    (call_script, "script_cf_sod_companion_campaign_available", "trp_npc7", sod_companion_campaign_mode_travel),
    (eq, "$g_sod_deshavi_trail_warning_pending", 1),
    (troop_slot_eq, "trp_npc7", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Deshavi, show me the trail before it goes cold.", "companion_depth_deshavi_tracks_pending",
  [
    (try_begin),
      (le, "$g_sod_deshavi_trail_focus_center", 0),
      (call_script, "script_sod_companion_select_focus_village", sod_companion_focus_trail_pressure),
      (assign, "$g_sod_deshavi_trail_focus_center", reg0),
      (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_target_center, "$g_sod_deshavi_trail_focus_center"),
      (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_last_center, "$g_sod_deshavi_trail_focus_center"),
      (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc7"),
    (try_end),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc7"),
    (main_party_has_troop, "trp_npc7"),
  ],
  "Deshavi, what are you seeing from the edge of camp?", "companion_depth_deshavi",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc7"),
  ]],
]
