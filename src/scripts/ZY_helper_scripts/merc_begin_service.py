# COST: low
SCRIPTS = [
("merc_begin_service",
 [
   (store_script_param_1, ":faction_no"),
   (store_script_param_2, ":signing_bonus"),
   (store_script_param, ":renew_days", 3),

   (call_script, "script_troop_add_gold", "trp_player", ":signing_bonus"),
   (store_current_hours, ":cur_hours"),
   (store_add, "$mercenary_service_next_pay_time", ":cur_hours", 7 * 24),
   (assign, "$mercenary_service_accumulated_pay", 0),
   (store_current_day, ":cur_day"),
   (store_add, "$mercenary_service_next_renew_day", ":cur_day", ":renew_days"),
   (call_script, "script_player_join_faction", ":faction_no"),
 ]),
]
