# COST: trivial
SCRIPTS = [
("cf_sod_center_can_hire_mercenary_hall_troops",
 [
   (store_script_param_1, ":center_no"),

   (is_between, ":center_no", castles_begin, castles_end),
   (party_slot_eq, ":center_no", slot_center_has_mercenary_guild_hall, 1),
   (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1),
   (party_slot_ge, ":center_no", slot_center_sod_merc_hall_troop_type, 1),
   (party_slot_ge, ":center_no", slot_center_sod_merc_hall_troop_amount, 1),
 ]),
]
