DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc16"),
    (main_party_has_troop, "trp_npc16"),
    (call_script, "script_cf_sod_companion_campaign_available", "trp_npc16", sod_companion_campaign_mode_dialog),
    (eq, "$g_sod_klethi_old_job_pending", 1),
    (troop_slot_eq, "trp_npc16", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Klethi, tell me whose old work found your knife.", "companion_depth_klethi_knife_pending",
  []],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc16"),
    (main_party_has_troop, "trp_npc16"),
  ],
  "Klethi, what are you not saying?", "companion_depth_klethi",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc16"),
  ]],
]
