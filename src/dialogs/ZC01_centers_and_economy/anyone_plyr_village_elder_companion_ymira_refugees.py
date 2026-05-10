DIALOGS = [
[anyone|plyr, "village_elder_talk",
  [
    (main_party_has_troop, "trp_npc3"),
    (call_script, "script_cf_sod_companion_campaign_available", "trp_npc3", sod_companion_campaign_mode_dialog),
    (eq, "$current_town", "$g_sod_ymira_refugee_focus_center"),
    (eq, "$g_sod_ymira_refugee_confronted", 0),
    (this_or_next|troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_trust_unlocked),
    (troop_slot_eq, "trp_npc3", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
    (party_count_members_of_type, ":male_slaves", "p_main_party", "trp_slave"),
    (party_count_members_of_type, ":female_slaves", "p_main_party", "trp_slave_female"),
    (store_add, ":slave_count", ":male_slaves", ":female_slaves"),
    (val_max, ":slave_count", "$g_sod_ymira_refugee_captive_count"),
    (ge, ":slave_count", 3),
  ],
  "Ymira says some captives may find shelter here. Will the village hear them?", "village_elder_companion_ymira_refugees",
  []],
]
