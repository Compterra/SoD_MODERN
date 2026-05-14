SCRIPTS = [
("set_player_relation_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":relation"),

      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (try_begin),
        (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
        (lt, ":player_relation", 0),
        (ge, ":relation", 0),
        (assign, ":relation", -1),
      (try_end),
      (store_sub, ":reln_dif", ":relation", ":player_relation"),
      (call_script, "script_change_player_relation_with_faction", ":faction_no", ":reln_dif"),
  ]),
]
