SCRIPTS = [
("get_num_tournament_participants",
        [(assign, ":num_participants", 0),
          (try_for_range, ":cur_slot", 0, 64),
            (troop_slot_ge, "trp_tournament_participants", ":cur_slot", 0),
            (val_add, ":num_participants", 1),
          (try_end),
          (assign, reg0, ":num_participants"),
      ]),
]
