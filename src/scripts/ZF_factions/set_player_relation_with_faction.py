SCRIPTS = [
("set_player_relation_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":relation"),

      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (store_sub, ":reln_dif", ":relation", ":player_relation"),
      (call_script, "script_change_player_relation_with_faction", ":faction_no", ":reln_dif"),
  ]),
]
