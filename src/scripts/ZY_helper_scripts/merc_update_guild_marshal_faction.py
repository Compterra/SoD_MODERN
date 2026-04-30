# COST: trivial
SCRIPTS = [
("merc_update_guild_marshal_faction",
 [
   (store_script_param_1, ":guild_no"),
   (store_script_param_2, ":target_faction"),

   (try_begin),
     (gt, ":guild_no", 0),
     (faction_get_slot, ":faction_base", ":guild_no", slot_guild_base),
     (gt, ":faction_base", 0),
     (party_get_slot, ":faction_marshal", ":faction_base", slot_town_lord),
     (gt, ":faction_marshal", 0),
     (troop_get_slot, ":lord_party", ":faction_marshal", slot_troop_leaded_party),
     (gt, ":lord_party", 0),
     (party_set_faction, ":lord_party", ":target_faction"),
   (try_end),
 ]),
]
