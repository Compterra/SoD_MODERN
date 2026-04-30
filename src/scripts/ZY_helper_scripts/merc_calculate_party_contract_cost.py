# COST: low
SCRIPTS = [
("merc_calculate_party_contract_cost",
 [
   (store_script_param_1, ":party_no"),
   (store_script_param_2, ":term_months"),

   (assign, ":total_cost", 0),
   (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
   (try_for_range, ":i_stack", 0, ":num_stacks"),
     (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
     (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
     (call_script, "script_game_get_join_cost", ":stack_troop"),
     (assign, ":cur_cost", reg0),
     (val_mul, ":cur_cost", ":stack_size"),
     (val_add, ":total_cost", ":cur_cost"),
   (try_end),

   (party_get_slot, ":guild_faction", ":party_no", slot_party_orginal_faction),
   (try_begin),
     (gt, ":guild_faction", 0),
     (call_script, "script_merc_get_guild_price_factor", ":guild_faction"),
     (val_mul, ":total_cost", reg0),
     (val_div, ":total_cost", 100),
     (call_script, "script_merc_get_relation_price_factor", ":guild_faction"),
     (val_mul, ":total_cost", reg0),
     (val_div, ":total_cost", 100),
   (try_end),

   (try_begin),
     (ge, ":term_months", 6),
     (val_mul, ":total_cost", 420),
     (val_div, ":total_cost", 100),
   (else_try),
     (ge, ":term_months", 3),
     (val_mul, ":total_cost", 255),
     (val_div, ":total_cost", 100),
   (try_end),

   (assign, reg0, ":total_cost"),
 ]),
]
