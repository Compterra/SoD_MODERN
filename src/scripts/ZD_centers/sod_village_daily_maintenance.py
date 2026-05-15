# COST: light
SCRIPTS = [
("sod_village_daily_refresh_merchant_inventories",
 [
   (try_for_range, ":village_no", villages_begin, villages_end),
     (call_script, "script_refresh_village_merchant_inventory", ":village_no"),
   (try_end),
 ]),

("sod_village_refresh_defenders_and_cattle_flags",
 [
   (try_for_range, ":village_no", villages_begin, villages_end),
     (call_script, "script_refresh_village_defenders", ":village_no"),
     (party_set_slot, ":village_no", slot_village_player_can_not_steal_cattle, 0),
   (try_end),
 ]),
]
