DIALOGS = [
[trp_sod_marshal, "marshal_location_show",
    [
      (call_script, "script_update_troop_location_notes", "$hero_requested_to_learn_location", 1),
      (call_script, "script_get_information_about_troops_position", "$hero_requested_to_learn_location", 0),
    ],
    "{s1}", "marshal_talk",
    []],
]
