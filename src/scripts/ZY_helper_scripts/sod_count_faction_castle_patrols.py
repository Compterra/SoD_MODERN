# COST: party scan
SCRIPTS = [
("sod_count_faction_castle_patrols",
 [
   (store_script_param, ":faction_no", 1),
   (assign, reg0, 0),
   (try_for_parties, ":cur_party"),
     (party_slot_eq, ":cur_party", slot_party_sod_support_type, sod_support_type_castle_patrol),
     (party_slot_eq, ":cur_party", slot_party_type, spt_patrol),
     (store_faction_of_party, ":party_faction", ":cur_party"),
     (eq, ":party_faction", ":faction_no"),
     (party_get_slot, ":status", ":cur_party", slot_party_sod_patrol_status),
     (this_or_next|eq, ":status", sod_castle_patrol_status_forming),
     (this_or_next|eq, ":status", sod_castle_patrol_status_active),
     (eq, ":status", sod_castle_patrol_status_damaged),
     (val_add, reg0, 1),
   (try_end),
 ]),
]
