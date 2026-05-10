# COST: low
SCRIPTS = [
("sod_threat_board_fail_contract",
 [
   (try_begin),
     (check_quest_active, "qst_regional_threat_contract"),

    (quest_get_slot, ":threat_type", "qst_regional_threat_contract", slot_quest_sod_threat_type),
    (quest_get_slot, ":sponsor_center", "qst_regional_threat_contract", slot_quest_sod_threat_sponsor_center),
    (quest_get_slot, ":target_party", "qst_regional_threat_contract", slot_quest_sod_threat_target_party),
    (call_script, "script_sod_threat_board_clear_target_party_link", ":target_party"),

    (try_begin),
      (gt, ":target_party", 0),
      (party_is_active, ":target_party"),
      (party_get_slot, ":active_quest", ":target_party", slot_party_sod_threat_active_quest),
      (eq, ":active_quest", "qst_regional_threat_contract"),
      (remove_party, ":target_party"),
    (try_end),
    (call_script, "script_sod_threat_board_normalize_center", ":sponsor_center"),
    (assign, ":sponsor_center", reg0),
     (call_script, "script_sod_threat_board_apply_regional_pressure", ":threat_type", ":sponsor_center"),
     (call_script, "script_fail_quest", "qst_regional_threat_contract"),
     (call_script, "script_end_quest", "qst_regional_threat_contract"),
     (call_script, "script_sod_threat_board_init_registry"),
    (display_message, "@Job board contract failed; local confidence falls.", 0xFFCC66),
   (else_try),
     (display_message, "@No active job board contract was found to fail.", 0xCC4444),
   (try_end),
 ]),
]
