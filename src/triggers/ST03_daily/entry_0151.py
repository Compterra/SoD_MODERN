SIMPLE_TRIGGERS = [
(24,
 [
   (try_begin),
     (check_quest_active, "qst_regional_threat_contract"),
     (quest_slot_eq, "qst_regional_threat_contract", slot_quest_sod_threat_ready_to_claim, 0),

     (quest_get_slot, ":target_party", "qst_regional_threat_contract", slot_quest_sod_threat_target_party),
     (quest_get_slot, ":deadline", "qst_regional_threat_contract", slot_quest_sod_threat_deadline_day),
     (store_current_day, ":cur_day"),

     (try_begin),
       (ge, ":cur_day", ":deadline"),
       (call_script, "script_sod_threat_board_fail_contract"),
     (else_try),
       (gt, ":target_party", 0),
       (neg|party_is_active, ":target_party"),
       (call_script, "script_sod_threat_board_fail_contract"),
     (else_try),
       (le, ":target_party", 0),
       (call_script, "script_sod_threat_board_fail_contract"),
     (try_end),
   (try_end),
 ]),
]
