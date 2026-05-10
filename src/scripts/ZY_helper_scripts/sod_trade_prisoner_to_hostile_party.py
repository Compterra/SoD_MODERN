# COST: light
SCRIPTS = [
("sod_trade_prisoner_to_hostile_party",
 [
   (store_script_param, ":target_party", 1),
   (call_script, "script_sod_has_tradeable_hostile_prisoner"),
   (assign, ":prisoner_troop", "$g_sod_hostile_trade_prisoner_troop"),
   (try_begin),
     (eq, reg0, 1),
     (party_remove_prisoners, "p_main_party", ":prisoner_troop", 1),
     (party_add_prisoners, ":target_party", ":prisoner_troop", 1),
     (assign, reg0, 1),
   (else_try),
     (assign, reg0, 0),
   (try_end),
 ]),
]
