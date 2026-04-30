DIALOGS = [
[anyone|plyr|repeat_for_troops, "tavern_traveler_pretender_location_ask",
   [
     (store_repeat_object, ":troop_no"),
     (is_between, ":troop_no", pretenders_begin, pretenders_end),
     (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
     (troop_slot_ge, ":troop_no", slot_troop_cur_center, 1),
     (call_script, "script_store_troop_name", s11, ":troop_no"),
     (neq, ":troop_no", "$supported_pretender"),
     ],  "{s11}", "tavern_traveler_pretender_location_ask_2",
   [
     (store_repeat_object, "$temp"),
     ]],
]
