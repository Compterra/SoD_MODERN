# COST: trivial
SCRIPTS = [
("cf_sod_merc_guild_uses_classic_employer_rotation",
 [
   (store_script_param_1, ":guild_faction"),
   # Guilds 1-5 use the legacy kingdom-employer rotation. Slavers and Boar Clan
   # use special world-presence systems and should not be pulled into this loop.
   (is_between, ":guild_faction", guilds_begin, "fac_sod_merc_guild6"),
 ]),
]
