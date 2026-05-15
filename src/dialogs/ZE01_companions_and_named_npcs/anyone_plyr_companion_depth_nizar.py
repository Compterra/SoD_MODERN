DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc13"),
    (main_party_has_troop, "trp_npc13"),
    (eq, "$g_sod_nizar_charge_pending", 1),
    (eq, "$g_sod_nizar_charge_confronted", 1),
    (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Nizar, show me the charge before it becomes a song.", "companion_depth_nizar_charge_pending",
  []],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc13"),
    (main_party_has_troop, "trp_npc13"),
  ],
  "Nizar, is this campaign worthy of song?", "companion_depth_nizar",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc13"),
  ]],
]
