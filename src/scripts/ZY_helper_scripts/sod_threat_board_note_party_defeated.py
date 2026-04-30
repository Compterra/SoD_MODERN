# COST: trivial
SCRIPTS = [
("sod_threat_board_note_party_defeated",
 [
   (store_script_param_1, ":party_no"),

   (try_begin),
     (check_quest_active, "qst_regional_threat_contract"),
     (quest_slot_eq, "qst_regional_threat_contract", slot_quest_sod_threat_target_party, ":party_no"),
     (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_ready_to_claim, 1),
     (call_script, "script_succeed_quest", "qst_regional_threat_contract"),
     (display_message, "@The marked threat has been broken. Return to any regional board to claim the reward.", 0x66CC66),
   (try_end),
 ]),
]
