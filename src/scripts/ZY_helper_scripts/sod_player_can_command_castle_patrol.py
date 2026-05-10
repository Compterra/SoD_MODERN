# COST: low
SCRIPTS = [
("sod_player_can_command_castle_patrol",
 [
   (store_script_param, ":patrol_party", 1),
   (assign, reg0, 0),
   (try_begin),
     (party_slot_eq, ":patrol_party", slot_party_sod_support_type, sod_support_type_castle_patrol),
     (party_get_slot, ":origin", ":patrol_party", slot_party_sod_patrol_origin_castle),
     (gt, ":origin", 0),
     (store_faction_of_party, ":patrol_faction", ":patrol_party"),
     (party_get_slot, ":lord", ":origin", slot_town_lord),
     (try_begin),
       (eq, ":lord", "trp_player"),
       (assign, reg0, 1),
     (else_try),
       (gt, "$players_kingdom", 0),
       (eq, ":patrol_faction", "$players_kingdom"),
       (assign, reg0, 1),
     (try_end),
   (try_end),
 ]),
]
