DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc6"),
    (main_party_has_troop, "trp_npc6"),
    (call_script, "script_cf_sod_companion_campaign_available", "trp_npc6", sod_companion_campaign_mode_dialog),
    (eq, "$g_sod_firentis_restitution_pending", 1),
    (troop_slot_eq, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Firentis, tell me what restitution still asks of us.", "companion_depth_firentis_restitution_pending",
  [
    (try_begin),
      (le, "$g_sod_firentis_restitution_focus_center", 0),
      (call_script, "script_sod_companion_select_focus_village", sod_companion_focus_restitution_village),
      (assign, "$g_sod_firentis_restitution_focus_center", reg0),
    (try_end),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc6"),
    (main_party_has_troop, "trp_npc6"),
    (call_script, "script_cf_sod_companion_campaign_available", "trp_npc6", sod_companion_campaign_mode_dialog),
  ],
  "Firentis, how does the company sit with your conscience?", "companion_depth_firentis",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc6"),
  ]],
]
