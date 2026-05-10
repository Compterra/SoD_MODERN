# COST: low
SCRIPTS = [
("sod_has_tradeable_hostile_prisoner",
 [
   (assign, reg0, 0),
   (assign, "$g_sod_hostile_trade_prisoner_troop", -1),
   (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
   (try_for_range, ":stack_no", 0, ":num_stacks"),
     (eq, reg0, 0),
     (party_prisoner_stack_get_troop_id, ":troop_id", "p_main_party", ":stack_no"),
     (neg|troop_is_hero, ":troop_id"),
     (assign, "$g_sod_hostile_trade_prisoner_troop", ":troop_id"),
     (assign, reg0, 1),
   (try_end),
 ]),
]
