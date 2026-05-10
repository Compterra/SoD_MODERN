DIALOGS = [
[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc11"),
    (main_party_has_troop, "trp_npc11"),
    (eq, "$g_sod_katrin_last_coin_pending", 1),
    (eq, "$g_sod_katrin_last_coin_confronted", 1),
    (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Katrin, put the ledger in my hands. What must be settled?", "companion_depth_katrin_coin_pending",
  []],

[anyone|plyr, "member_talk",
  [
    (eq, "$g_talk_troop", "trp_npc11"),
    (main_party_has_troop, "trp_npc11"),
  ],
  "Katrin, what does the camp need from me?", "companion_depth_katrin",
  [
    (call_script, "script_sod_companion_try_trigger_reaction", "trp_npc11"),
  ]],
]
