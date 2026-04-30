DIALOGS = [
[anyone, "tavern_traveler_companion_location_tell", [], "{s15} is currently at {s11}.", "tavern_traveler_pretalk",
   [
     (call_script, "script_store_troop_name", s15, "$temp"),
     (troop_get_slot, ":cur_center", "$temp", slot_troop_cur_center),
     (str_store_party_name, s11, ":cur_center"),
     ]],
]
