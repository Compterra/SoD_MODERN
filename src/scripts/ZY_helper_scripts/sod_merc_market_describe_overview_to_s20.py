# COST: medium
SCRIPTS = [
("sod_merc_market_describe_overview_to_s20",
 [
   (call_script, "script_sod_merc_guild_repair_ledgers"),
   (call_script, "script_sod_merc_market_refresh_kingdom_demands"),
   (str_store_string, s50, "@Mercenary Market Overview^^Kingdom bids:"),
   (try_for_range, ":kingdom_faction", kingdoms_begin, kingdoms_end),
     (neq, ":kingdom_faction", "fac_kingdom_6"),
     (faction_slot_eq, ":kingdom_faction", slot_faction_state, sfs_active),
     (call_script, "script_sod_merc_market_describe_kingdom_demand_to_s20", ":kingdom_faction"),
     (faction_get_slot, ":last_hired_guild", ":kingdom_faction", slot_faction_sod_merc_last_hired_guild),
     (try_begin),
       (is_between, ":last_hired_guild", guilds_begin, guilds_end),
       (str_store_faction_name, s51, ":last_hired_guild"),
       (str_store_string, s50, "@{s50}^{s20} Last accepted guild: {s51}."),
     (else_try),
       (str_store_string, s50, "@{s50}^{s20} No recent guild hire recorded."),
     (try_end),
   (try_end),

   (str_store_string, s50, "@{s50}^^Guild ledgers:"),
   (try_for_range, ":guild_faction", guilds_begin, guilds_end),
     (call_script, "script_cf_sod_faction_is_merc_guild", ":guild_faction"),
     (call_script, "script_sod_merc_guild_describe_ledger_to_s20", ":guild_faction"),
     (str_store_string, s50, "@{s50}^{s20}"),
   (try_end),

   (str_store_string, s20, s50),
 ]),
]
