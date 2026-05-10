DIALOGS = [
[anyone|plyr, "regular_member_talk",
  [
    (main_party_has_troop, "trp_npc11"),
    (eq, "$g_sod_katrin_last_coin_pending", 1),
    (eq, "$g_sod_katrin_last_coin_witnessed", 0),
    (eq, "$g_sod_katrin_last_coin_confronted", 0),
    (troop_slot_eq, "trp_npc11", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Katrin says the ledger has reached the campfires. What are people saying?", "regular_member_companion_katrin_ledger", []],
]
