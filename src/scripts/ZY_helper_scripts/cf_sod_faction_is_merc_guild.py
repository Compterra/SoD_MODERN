# COST: trivial
SCRIPTS = [
("cf_sod_faction_is_merc_guild",
 [
   (store_script_param_1, ":faction_no"),
   (is_between, ":faction_no", guilds_begin, guilds_end),
 ]),
]
