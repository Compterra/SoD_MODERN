# COST: low
SCRIPTS = [
("sod_threat_board_clear_target_party_link",
 [
   (store_script_param_1, ":target_party"),

   (try_begin),
     (gt, ":target_party", 0),
     (party_is_active, ":target_party"),
     (party_set_slot, ":target_party", slot_party_sod_threat_active_quest, 0),
   (try_end),
 ]),
]
