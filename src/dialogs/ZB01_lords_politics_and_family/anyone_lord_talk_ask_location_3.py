DIALOGS = [
[anyone, "lord_talk_ask_location_3",
   [(call_script, "script_update_troop_location_notes", "$hero_requested_to_learn_location", 1),
    (call_script, "script_get_information_about_troops_position", "$hero_requested_to_learn_location", 0),
   ],
   "{s1}", "lord_pretalk", []],
]
