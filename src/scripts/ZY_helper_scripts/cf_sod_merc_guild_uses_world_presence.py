# COST: trivial
SCRIPTS = [
("cf_sod_merc_guild_uses_world_presence",
 [
   (store_script_param_1, ":guild_faction"),
   (call_script, "script_cf_sod_faction_is_merc_guild", ":guild_faction"),
 ]),
]
