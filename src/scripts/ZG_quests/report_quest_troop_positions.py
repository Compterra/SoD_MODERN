SCRIPTS = [
("report_quest_troop_positions",
      [(store_script_param, ":quest_no", 1),
        (store_script_param, ":troop_no", 2),
        (store_script_param, ":note_index", 3),
        (call_script, "script_get_information_about_troops_position", ":troop_no", 1),
        (str_store_string, s5, "@At the time quest was given:^{s1}"),
        (add_quest_note_from_sreg, ":quest_no", ":note_index", s5, 1),
        (call_script, "script_update_troop_location_notes", ":troop_no", 1),
    ]),
]
