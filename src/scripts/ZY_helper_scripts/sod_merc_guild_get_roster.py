# COST: trivial
SCRIPTS = [
("sod_merc_guild_get_roster",
 [
   (store_script_param_1, ":guild_faction"),

   (assign, reg0, 0),
   (assign, reg1, 0),
   (assign, reg2, 0),
   (assign, reg3, 0),
   (try_begin),
     (call_script, "script_cf_sod_faction_is_merc_guild", ":guild_faction"),
     (faction_get_slot, reg0, ":guild_faction", slot_guild_tier_1_unit_1),
     (faction_get_slot, reg1, ":guild_faction", slot_guild_tier_1_unit_2),
     (faction_get_slot, reg2, ":guild_faction", slot_guild_noble),
     (faction_get_slot, reg3, ":guild_faction", slot_guild_troop_proportion),
   (try_end),
 ]),
]
