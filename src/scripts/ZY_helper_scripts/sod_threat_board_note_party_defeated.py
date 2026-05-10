# COST: trivial
SCRIPTS = [
("sod_threat_board_note_party_defeated",
 [
   (store_script_param_1, ":party_no"),

  (try_begin),
    (gt, ":party_no", 0),
    (party_is_active, ":party_no"),
    (check_quest_active, "qst_regional_threat_contract"),
    (quest_slot_eq, "qst_regional_threat_contract", slot_quest_sod_threat_target_party, ":party_no"),
    (call_script, "script_sod_threat_board_clear_target_party_link", ":party_no"),
    (quest_set_slot, "qst_regional_threat_contract", slot_quest_sod_threat_ready_to_claim, 1),
    (str_store_party_name, s5, ":party_no"),
    (str_store_string, s6, "@Target defeated: {s5}. Claim payment at any job board."),
    (add_quest_note_from_sreg, "qst_regional_threat_contract", 5, s6, 0),
     (display_message, "@Target defeated. Claim payment at any job board.", 0x66CC66),
   (try_end),
 ]),
]
