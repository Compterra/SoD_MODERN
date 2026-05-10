DIALOGS = [
[anyone|plyr, "village_elder_talk",
  [
    (main_party_has_troop, "trp_npc6"),
    (call_script, "script_cf_sod_companion_campaign_available", "trp_npc6", sod_companion_campaign_mode_dialog),
    (eq, "$g_sod_firentis_restitution_pending", 1),
    (eq, "$current_town", "$g_sod_firentis_restitution_focus_center"),
    (eq, "$g_sod_firentis_restitution_witnessed", 0),
    (eq, "$g_sod_firentis_restitution_confronted", 0),
    (troop_slot_eq, "trp_npc6", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Firentis says this village is owed more than a victory. What would restitution mean here?", "village_elder_companion_firentis_restitution", []],
]
