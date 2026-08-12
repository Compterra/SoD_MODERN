# COST: low
SCRIPTS = [
("sod_merc_market_select_preferred_guild",
 [
   (store_script_param_1, ":kingdom_faction"),
   (store_script_param, ":use_cached_contract_totals", 2),
   (store_script_param, ":demand_type", 3),

   (assign, ":preferred_guild", 0),
   (assign, ":best_weight", -100),

   (try_begin),
     (is_between, ":kingdom_faction", native_kingdoms_begin, native_kingdoms_end),
     (faction_slot_eq, ":kingdom_faction", slot_faction_state, sfs_active),
     (faction_get_slot, ":pact_guild", ":kingdom_faction", slot_faction_merc_pact),
     (try_begin),
       (is_between, ":pact_guild", guilds_begin, guilds_end),
       (assign, ":preferred_guild", ":pact_guild"),
       (call_script, "script_sod_merc_market_calculate_kingdom_guild_weight", ":kingdom_faction", ":pact_guild", ":use_cached_contract_totals", ":demand_type"),
       (assign, ":best_weight", reg0),
     (try_end),

     (try_for_range, ":guild_faction", guilds_begin, guilds_end),
       (call_script, "script_sod_merc_market_calculate_kingdom_guild_weight", ":kingdom_faction", ":guild_faction", ":use_cached_contract_totals", ":demand_type"),
       (assign, ":cur_weight", reg0),
       (gt, ":cur_weight", ":best_weight"),
       (assign, ":best_weight", ":cur_weight"),
       (assign, ":preferred_guild", ":guild_faction"),
     (try_end),

     (try_begin),
       (lt, ":best_weight", -40),
       (assign, ":preferred_guild", 0),
     (try_end),
   (try_end),

   (assign, reg0, ":preferred_guild"),
   (assign, reg1, ":best_weight"),
 ]),
]
