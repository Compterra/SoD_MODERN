# COST: low
SCRIPTS = [
("sod_count_mercenary_guild_halls_for_guild",
 [
   (store_script_param_1, ":guild_faction"),

   (assign, ":hall_count", 0),
   (assign, ":player_hall_count", 0),
   (assign, ":stock_total", 0),
   (try_begin),
     (call_script, "script_cf_sod_faction_is_merc_guild", ":guild_faction"),
     (try_for_range, ":center_no", castles_begin, castles_end),
       (party_slot_eq, ":center_no", slot_party_type, spt_castle),
       (party_slot_eq, ":center_no", slot_center_has_mercenary_guild_hall, 1),
       (store_faction_of_party, ":center_faction", ":center_no"),
       (faction_slot_eq, ":center_faction", slot_faction_merc_pact, ":guild_faction"),
       (val_add, ":hall_count", 1),
       (try_begin),
         (this_or_next|eq, ":center_faction", "fac_player_faction"),
         (eq, ":center_faction", "fac_player_supporters_faction"),
         (val_add, ":player_hall_count", 1),
       (try_end),
       (party_get_slot, ":stock", ":center_no", slot_center_sod_merc_hall_troop_amount),
       (val_max, ":stock", 0),
       (val_add, ":stock_total", ":stock"),
     (try_end),
   (try_end),

   (assign, reg0, ":hall_count"),
   (assign, reg1, ":player_hall_count"),
   (assign, reg2, ":stock_total"),
 ]),
]
