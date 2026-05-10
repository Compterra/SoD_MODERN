# COST: companion scan
SCRIPTS = [
("sod_get_companion_patrol_role_bonus",
 [
   (store_script_param, ":role", 1),
   (assign, reg0, 0),
   (try_for_range, ":companion", companions_begin, companions_end),
     (main_party_has_troop, ":companion"),
     (troop_slot_eq, ":companion", slot_troop_companion_role, ":role"),
     (val_add, reg0, 1),
   (try_end),
 ]),
]
