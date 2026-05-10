# COST: party scan
SCRIPTS = [
("sod_count_castle_patrols",
 [
   (store_script_param, ":origin_castle", 1),
   (assign, reg0, 0),
   (try_for_parties, ":cur_party"),
     (party_slot_eq, ":cur_party", slot_party_sod_support_type, sod_support_type_castle_patrol),
     (party_slot_eq, ":cur_party", slot_party_sod_patrol_origin_castle, ":origin_castle"),
     (party_slot_eq, ":cur_party", slot_party_type, spt_patrol),
     (party_get_slot, ":status", ":cur_party", slot_party_sod_patrol_status),
     (this_or_next|eq, ":status", sod_castle_patrol_status_forming),
     (this_or_next|eq, ":status", sod_castle_patrol_status_active),
     (eq, ":status", sod_castle_patrol_status_damaged),
     (val_add, reg0, 1),
   (try_end),
 ]),
]
