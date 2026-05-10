# COST: trivial
SCRIPTS = [
("sod_merc_guild_get_access_level",
 [
   (store_script_param_1, ":guild_faction"),
   (store_script_param_2, ":buyer_faction"),

   (assign, ":access", sod_merc_access_outsider),
   (try_begin),
     (call_script, "script_cf_sod_faction_is_merc_guild", ":guild_faction"),
     (store_relation, ":relation", ":guild_faction", ":buyer_faction"),
     (call_script, "script_merc_get_elite_relation_requirement", ":guild_faction"),
     (assign, ":elite_requirement", reg0),
     (try_begin),
       (ge, ":relation", 40),
       (assign, ":access", sod_merc_access_trusted),
     (else_try),
       (ge, ":relation", 30),
       (assign, ":access", sod_merc_access_service),
     (else_try),
       (ge, ":relation", ":elite_requirement"),
       (assign, ":access", sod_merc_access_elite),
     (else_try),
       (ge, ":relation", 10),
       (assign, ":access", sod_merc_access_promotion),
     (try_end),
   (try_end),

   (assign, reg0, ":access"),
 ]),
]
