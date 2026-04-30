SCRIPTS = [
("change_player_relation_with_faction",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":difference"),

      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (assign, reg1, ":player_relation"),
      (val_add, ":player_relation", ":difference"),
      (val_clamp, ":player_relation", -100, 101),
      (assign, reg2, ":player_relation"),
      (set_relation, ":faction_no", "fac_player_faction", ":player_relation"),
      (set_relation, ":faction_no", "fac_player_supporters_faction", ":player_relation"),

      (str_store_faction_name_link, s1, ":faction_no"),
      (store_sub, reg3, reg2, reg1),
      (try_begin),
        (gt, reg3, 0),
        (display_message, "str_faction_relation_increased", gain_relation_color),
        #(display_message, "@debug: script_change_player_relation_with_faction", debug_color),
      (else_try),
        (lt, reg3, 0),
        (display_message, "str_faction_relation_detoriated", lose_relation_color),
        #(display_message, "@debug: script_change_player_relation_with_faction", debug_color),
      (try_end),
      (call_script, "script_update_all_notes"),
  ]),
]
