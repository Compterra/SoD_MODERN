# COST: castle scan
SCRIPTS = [
("sod_get_faction_castle_patrol_cap",
 [
   (store_script_param, ":faction_no", 1),
   (assign, ":owned_castles", 0),
   (try_for_range, ":castle_no", castles_begin, castles_end),
     (store_faction_of_party, ":castle_faction", ":castle_no"),
     (eq, ":castle_faction", ":faction_no"),
     (val_add, ":owned_castles", 1),
   (try_end),
   (store_mul, ":cap", ":owned_castles", sod_castle_patrol_max_active),
   (val_max, ":cap", sod_castle_patrol_faction_min_soft_cap),
   (assign, reg0, ":cap"),
 ]),
]
