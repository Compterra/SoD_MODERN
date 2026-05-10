# COST: low
SCRIPTS = [
("sod_castle_patrol_seek_refuge",
 [
   (store_script_param, ":patrol_party", 1),
   (store_faction_of_party, ":faction_no", ":patrol_party"),
   (call_script, "script_get_closest_walled_center_of_faction", ":patrol_party", ":faction_no"),
   (assign, ":refuge", reg0),
   (try_begin),
     (gt, ":refuge", 0),
     (party_set_slot, ":patrol_party", slot_party_sod_patrol_status, sod_castle_patrol_status_returning),
     (party_set_ai_behavior, ":patrol_party", ai_bhvr_travel_to_party),
     (party_set_ai_object, ":patrol_party", ":refuge"),
     (assign, reg0, ":refuge"),
   (else_try),
     (party_get_slot, ":origin", ":patrol_party", slot_party_sod_patrol_origin_castle),
     (party_set_slot, ":patrol_party", slot_party_sod_patrol_status, sod_castle_patrol_status_returning),
     (party_set_ai_behavior, ":patrol_party", ai_bhvr_travel_to_party),
     (party_set_ai_object, ":patrol_party", ":origin"),
     (assign, reg0, ":origin"),
   (try_end),
 ]),
]
