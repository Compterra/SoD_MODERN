# COST: low
SCRIPTS = [
("sod_count_mercenary_guild_halls_for_faction",
 [
   (store_script_param_1, ":faction_no"),

   (assign, ":hall_count", 0),
   (assign, ":stock_total", 0),
   (try_for_range, ":center_no", castles_begin, castles_end),
     (party_slot_eq, ":center_no", slot_party_type, spt_castle),
     (party_slot_eq, ":center_no", slot_center_has_mercenary_guild_hall, 1),
     (store_faction_of_party, ":center_faction", ":center_no"),
     (eq, ":center_faction", ":faction_no"),
     (val_add, ":hall_count", 1),
     (party_get_slot, ":stock", ":center_no", slot_center_sod_merc_hall_troop_amount),
     (val_max, ":stock", 0),
     (val_add, ":stock_total", ":stock"),
   (try_end),

   (assign, reg0, ":hall_count"),
   (assign, reg1, ":stock_total"),
 ]),
]
