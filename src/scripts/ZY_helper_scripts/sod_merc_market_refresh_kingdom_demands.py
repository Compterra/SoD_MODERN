# COST: medium
SCRIPTS = [
("sod_merc_market_refresh_kingdom_demands",
 [
   (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
     (neq, ":faction_no", "fac_kingdom_6"),
     (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
     (call_script, "script_sod_merc_market_calculate_kingdom_demand", ":faction_no"),
   (try_end),
 ]),
]
