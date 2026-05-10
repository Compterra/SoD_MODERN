# COST: low
SCRIPTS = [
("sod_castle_patrol_target_overwhelming",
 [
   (store_script_param, ":patrol_party", 1),
   (store_script_param, ":target_party", 2),
   (assign, reg0, 0),
   (try_begin),
     (gt, ":target_party", 0),
     (party_is_active, ":target_party"),
     (party_get_num_companions, ":patrol_size", ":patrol_party"),
     (party_get_num_companions, ":target_size", ":target_party"),
     (store_mul, ":danger_size", ":patrol_size", 3),
     (this_or_next|gt, ":target_size", ":danger_size"),
     (gt, ":target_size", 60),
     (assign, reg0, 1),
   (try_end),
 ]),
]
