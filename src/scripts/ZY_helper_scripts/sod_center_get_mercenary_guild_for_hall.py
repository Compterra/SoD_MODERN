# COST: trivial
SCRIPTS = [
("sod_center_get_mercenary_guild_for_hall",
 [
   (store_script_param_1, ":center_no"),

   (assign, ":guild", 0),
   (assign, ":uses_vanilla_stock", 0),
   (try_begin),
     (is_between, ":center_no", castles_begin, castles_end),
     (party_slot_eq, ":center_no", slot_party_type, spt_castle),
     (party_slot_eq, ":center_no", slot_center_has_mercenary_guild_hall, 1),
     (store_faction_of_party, ":center_faction", ":center_no"),
     (try_begin),
       (gt, ":center_faction", 0),
       (faction_get_slot, ":guild", ":center_faction", slot_faction_merc_pact),
       (try_begin),
         (call_script, "script_cf_sod_faction_is_merc_guild", ":guild"),
       (else_try),
         (assign, ":guild", 0),
       (try_end),
     (try_end),
     (try_begin),
       (le, ":guild", 0),
       (assign, ":uses_vanilla_stock", 1),
     (try_end),
   (try_end),

   (assign, reg0, ":guild"),
   (assign, reg1, ":uses_vanilla_stock"),
 ]),
]
