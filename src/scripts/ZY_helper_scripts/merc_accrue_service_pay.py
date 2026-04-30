# COST: low
SCRIPTS = [
("merc_accrue_service_pay",
 [
   (store_current_hours, ":cur_hours"),
   (try_begin),
     (gt, "$mercenary_service_next_pay_time", 0),
     (gt, "$players_kingdom", 0),
     (neq, "$players_kingdom", "fac_player_supporters_faction"),
     (eq, "$player_has_homage", 0),
     (ge, ":cur_hours", "$mercenary_service_next_pay_time"),

     (call_script, "script_party_calculate_strength", "p_main_party", 0),
     (assign, ":offer_value", reg0),
     (val_div, ":offer_value", 2),
     (val_add, ":offer_value", 30),
     (call_script, "script_round_value", ":offer_value"),
     (val_add, "$mercenary_service_accumulated_pay", reg0),
     (store_add, "$mercenary_service_next_pay_time", ":cur_hours", 7 * 24),
   (try_end),
 ]),
]
