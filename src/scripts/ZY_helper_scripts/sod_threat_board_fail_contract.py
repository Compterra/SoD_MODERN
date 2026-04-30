# COST: low
SCRIPTS = [
("sod_threat_board_fail_contract",
 [
   (quest_get_slot, ":threat_type", "qst_regional_threat_contract", slot_quest_sod_threat_type),
   (quest_get_slot, ":sponsor_center", "qst_regional_threat_contract", slot_quest_sod_threat_sponsor_center),
   (quest_get_slot, ":target_party", "qst_regional_threat_contract", slot_quest_sod_threat_target_party),

   (try_begin),
     (party_is_active, ":target_party"),
     (remove_party, ":target_party"),
   (try_end),
   (call_script, "script_sod_threat_board_apply_regional_pressure", ":threat_type", ":sponsor_center"),
   (call_script, "script_fail_quest", "qst_regional_threat_contract"),
   (call_script, "script_end_quest", "qst_regional_threat_contract"),
   (call_script, "script_sod_threat_board_init_registry"),
   (display_message, "@A regional threat-board contract has expired. The sponsor loses confidence.", 0xFFCC66),
 ]),
]
