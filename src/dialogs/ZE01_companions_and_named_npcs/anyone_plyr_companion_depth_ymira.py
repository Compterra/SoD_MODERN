DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc3"),
    (main_party_has_troop, "trp_npc3"),
    (call_script, "script_cf_sod_companion_campaign_available", "trp_npc3", sod_companion_campaign_mode_dialog),
    (this_or_next|troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
    (party_count_members_of_type, ":male_slaves", "p_main_party", "trp_slave"),
    (party_count_members_of_type, ":female_slaves", "p_main_party", "trp_slave_female"),
    (store_add, ":slave_count", ":male_slaves", ":female_slaves"),
    (val_max, ":slave_count", "$g_sod_ymira_refugee_captive_count"),
    (ge, ":slave_count", 3),
  ],
  "Ymira, speak for the captives.", "companion_depth_ymira_captive_pending",
  [
    (try_begin),
      (le, "$g_sod_ymira_refugee_focus_center", 0),
      (call_script, "script_sod_companion_select_focus_village", sod_companion_focus_refugee_shelter),
      (assign, "$g_sod_ymira_refugee_focus_center", reg0),
    (try_end),
  ]],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc3"),
    (main_party_has_troop, "trp_npc3"),
    (call_script, "script_cf_sod_companion_campaign_available", "trp_npc3", sod_companion_campaign_mode_dialog),
  ],
  "Ymira, how is this road wearing on you?", "companion_depth_ymira",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc3"),
  ]],
]
