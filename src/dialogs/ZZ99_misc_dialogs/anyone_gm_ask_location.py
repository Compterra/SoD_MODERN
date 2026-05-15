DIALOGS = [
[anyone, "gm_ask_location", [
   (call_script, "script_update_troop_location_notes", "$hero_requested_to_learn_location", 1),
   (call_script, "script_get_information_about_troops_position", "$hero_requested_to_learn_location", 0),
   (str_store_string_reg, s68, s1),
    ], "{s68}", "gm_pretalk", []],
]
