DIALOGS = [
[anyone, "slaver_world_caravan_companion_deshavi_pursuer",
  [
    (try_begin),
      (gt, "$g_sod_deshavi_trail_focus_center", 0),
      (party_is_active, "$g_sod_deshavi_trail_focus_center"),
      (str_store_party_name_link, s3, "$g_sod_deshavi_trail_focus_center"),
    (else_try),
      (str_store_string, s3, "@the next hungry village"),
    (try_end),
  ],
  "A good hunter knows which footprints are coin and which are bait. If your wood-woman read us near {s3}, she read well. But reading tracks does not open cages.",
  "slaver_world_caravan_talk",
  [
    (assign, "$g_sod_deshavi_trail_witnessed", 1),
    (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_progress, 50),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_scout_warning, 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc7"),
    (display_message, "@A Slaver pursuer confirms Deshavi's trail. Tracks Through Ash now has a hunter witness.", 0x99CCFF),
  ]],
]
