DIALOGS = [
[anyone, "battle_reason_companion_nizar_charge",
  [],
  "There: dust to blind them, a hard left before their spears settle, and an exit before glory turns stupid. Beautiful things deserve planning, especially the dangerous ones.",
  "plyr_battle_reason",
  [
    (assign, "$g_sod_nizar_charge_witnessed", 1),
    (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_progress, 50),
    (quest_set_slot, "qst_companion_nizar_impossible_charge", slot_quest_sod_runtime_metadata, "$g_sod_nizar_charge_result_grade"),
    (call_script, "script_sod_companion_apply_player_action", sod_companion_action_tournament_glory, 1),
    (call_script, "script_sod_companion_sync_personal_quest_framework", "trp_npc13"),
    (display_message, "@Nizar sketches the impossible charge before battle. The Impossible Charge now has a field setup.", 0x99CCFF),
  ]],
]
