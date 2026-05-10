DIALOGS = [
[anyone|plyr, "plyr_battle_reason",
  [
    (main_party_has_troop, "trp_npc13"),
    (eq, "$g_sod_nizar_charge_pending", 1),
    (eq, "$g_sod_nizar_charge_witnessed", 0),
    (eq, "$g_sod_nizar_charge_confronted", 0),
    (troop_slot_eq, "trp_npc13", slot_troop_companion_personal_quest_stage, sod_companion_quest_test_started),
  ],
  "Nizar, mark the charge before the horns answer for us.", "battle_reason_companion_nizar_charge", []],
]
