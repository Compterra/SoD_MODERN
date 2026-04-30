DIALOGS = [
[anyone|plyr|repeat_for_troops, "tavern_traveler_companion_location_ask",
   [
     (store_repeat_object, ":troop_no"),
     (is_between, ":troop_no", companions_begin, companions_end),
     (troop_slot_ge, ":troop_no", slot_troop_cur_center, 1),
     (troop_slot_ge, ":troop_no", slot_troop_playerparty_history, 1),
     (call_script, "script_store_troop_name", s11, ":troop_no"),
     ],  "{s11}", "tavern_traveler_companion_location_ask_2",
   [
     (store_repeat_object, "$temp"),
     ]],
]
