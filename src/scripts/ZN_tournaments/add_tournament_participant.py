SCRIPTS = [
("add_tournament_participant",
        [(store_script_param, ":troop_no", 1),
          (assign, ":continue", 1),
          (try_for_range, ":cur_slot", 0, 64),
            (eq, ":continue", 1),
            (troop_slot_eq, "trp_tournament_participants", ":cur_slot", -1),
            (troop_set_slot, "trp_tournament_participants", ":cur_slot", ":troop_no"),
            (assign, ":continue", 0),
          (try_end),
      ]),
]
