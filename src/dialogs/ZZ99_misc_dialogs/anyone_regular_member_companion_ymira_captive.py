DIALOGS = [
[anyone, "regular_member_companion_ymira_captive",
  [
    (try_begin),
      (gt, "$g_sod_ymira_refugee_focus_center", 0),
      (party_is_active, "$g_sod_ymira_refugee_focus_center"),
      (str_store_party_name_link, s3, "$g_sod_ymira_refugee_focus_center"),
    (else_try),
      (str_store_string, s3, "@any door that will take a frightened name"),
    (try_end),
  ],
  "Then hear this: chains teach a person to answer quickly and hope slowly. The healer-woman asked my name. If you mean mercy, let it have a road to {s3}, not only a kind word beside the wagons.",
  "regular_member_talk",
  [
    (assign, "$g_sod_ymira_refugee_witnessed", 1),
    (quest_set_slot, "qst_companion_ymira_mercy_under_arms", slot_quest_sod_runtime_progress, 50),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_ymira_refugee_mercy, 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc3"),
    (display_message, "@A captive speaks for Ymira's refugees. Mercy Under Arms now has a direct witness.", 0x99CCFF),
  ]],
]
