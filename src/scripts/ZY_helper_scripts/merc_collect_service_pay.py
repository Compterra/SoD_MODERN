# COST: trivial
SCRIPTS = [
("merc_collect_service_pay",
 [
   (try_begin),
     (gt, "$mercenary_service_accumulated_pay", 0),
     (troop_add_gold, "trp_player", "$mercenary_service_accumulated_pay"),
     (assign, "$mercenary_service_accumulated_pay", 0),
   (try_end),
 ]),
]
