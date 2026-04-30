SCRIPTS = [
("get_number_of_factions_at_war_with_faction",

  [     (store_script_param_1, ":faction_no"),

        (assign, ":num_opponents", 0),

        (try_for_range, ":faction2_no", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction2_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", ":faction2_no"),
        (store_relation, ":rln", ":faction_no", ":faction2_no"),
          (try_begin),
          (lt, ":rln", 0),
          (val_add, ":num_opponents", 1),
          (try_end),
        (try_end),

        (assign, reg0, ":num_opponents"),
   ]),
]
