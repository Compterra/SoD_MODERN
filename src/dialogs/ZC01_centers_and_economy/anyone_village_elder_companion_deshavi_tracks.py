DIALOGS = [
[anyone, "village_elder_companion_deshavi_tracks",
  [
    (try_begin),
      (eq, "$g_sod_deshavi_trail_warning_cause", 2),
      (str_store_string, s4, "@people with rope-burned wrists and men asking after them too loudly"),
    (else_try),
      (str_store_string, s4, "@hungry families who would not enter by the road"),
    (try_end),
    (party_is_active, "$current_town"),
    (str_store_party_name_link, s3, "$current_town"),
  ],
  "Near {s3}, we saw {s4}. Your tracker has the truth of it. The tracks are not old enough to be memory yet.",
  "village_elder_talk",
  [
    (assign, "$g_sod_deshavi_trail_witnessed", 1),
    (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_last_center, "$current_town"),
    (quest_set_slot, "qst_companion_deshavi_tracks_through_ash", slot_quest_sod_runtime_progress, 50),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_scout_warning, 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc7"),
    (display_message, "@The village elder confirms Deshavi's trail. Tracks Through Ash now has witnesses, not only signs.", 0x99CCFF),
  ]],
]
