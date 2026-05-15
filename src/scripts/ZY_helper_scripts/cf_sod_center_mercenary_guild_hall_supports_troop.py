# COST: trivial
SCRIPTS = [
("cf_sod_center_mercenary_guild_hall_supports_troop",
 [
   (store_script_param, ":center_no", 1),
   (store_script_param, ":troop_no", 2),

   (is_between, ":center_no", castles_begin, castles_end),
   (party_slot_eq, ":center_no", slot_party_type, spt_castle),
   (party_slot_eq, ":center_no", slot_center_has_mercenary_guild_hall, 1),
   (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
   (store_troop_faction, ":troop_faction", ":troop_no"),
   (call_script, "script_cf_sod_faction_is_merc_guild", ":troop_faction"),
   (store_faction_of_party, ":center_faction", ":center_no"),
   (faction_get_slot, ":pact_guild", ":center_faction", slot_faction_merc_pact),
   (eq, ":pact_guild", ":troop_faction"),
   (call_script, "script_sod_merc_market_calculate_guild_supply", ":troop_faction", 0),
   (assign, ":available_companies", reg0),
   (assign, ":max_company_size", reg1),
   (assign, ":refusal_reason", reg6),
   (gt, ":available_companies", 0),
   (ge, ":max_company_size", 20),
   (eq, ":refusal_reason", sod_merc_refusal_none),
 ]),
]
