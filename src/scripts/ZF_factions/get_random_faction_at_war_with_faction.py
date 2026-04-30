SCRIPTS = [
("get_random_faction_at_war_with_faction",

   [    (store_script_param_1, ":faction_no"),

        (call_script, "script_get_number_of_factions_at_war_with_faction", ":faction_no"),
        (assign, ":num_opponents", reg0), 
        
        (try_begin),
        (gt, ":num_opponents", 1),
        (store_random_in_range, ":rnd", 0, ":num_opponents"),
        (assign, ":opponent_number", 0), 
        (else_try),
        (assign, ":rnd", 0),
        (try_end),

        (try_for_range, ":faction2_no", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction2_no", slot_faction_state, sfs_active),
        (neq, ":faction_no", ":faction2_no"),
        (store_relation, ":rln", ":faction_no", ":faction2_no"),
          (try_begin),
          (lt, ":rln", 0),
          (eq, ":opponent_number", ":rnd"),
          (assign, ":chosen_opponent", ":faction2_no"),
          (val_add, ":opponent_number", 1),
          (else_try),
          (lt, ":rln", 0),
          (val_add, ":opponent_number", 1),
          (try_end),
        (try_end),

        (assign, reg0, ":chosen_opponent"),
]),
]
