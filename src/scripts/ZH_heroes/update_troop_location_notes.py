SCRIPTS = [
("update_troop_location_notes",
      [(store_script_param, ":troop_no", 1),
        (store_script_param, ":see_or_hear", 2),
        (str_clear, s49),
        (add_troop_note_from_sreg, ":troop_no", 2, s49, 0),
        (call_script, "script_get_information_about_troops_position", ":troop_no", 1),
        (try_begin),
          (neq, reg0, 0),
          (troop_get_type, reg1, ":troop_no"),
          (try_begin),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_dead),
			(str_store_string, s49, "@{reg1?She:He} is dead."),

			(add_troop_note_from_sreg, ":troop_no", 2, s49, 1),
		  (else_try),
            (eq, ":see_or_hear", 0),
            (str_store_string, s49, "@The last time you saw {reg1?her:him}, {s1}"),

            (add_troop_note_from_sreg, ":troop_no", 2, s49, 1),
          (else_try),
            (str_store_string, s49, "@The last time you heard about {reg1?her:him}, {s1}"),

            (add_troop_note_from_sreg, ":troop_no", 2, s49, 1),
          (try_end),
        (try_end),
    ]),
]
