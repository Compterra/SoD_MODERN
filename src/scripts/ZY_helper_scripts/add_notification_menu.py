SCRIPTS = [
("add_notification_menu",
    [
      (store_script_param, ":menu_no", 1),
      (store_script_param, ":menu_var_1", 2),
      (store_script_param, ":menu_var_2", 3),
      (assign, ":end_cond", 1),
      (try_for_range, ":cur_slot", 0, ":end_cond"),
        (try_begin),
          (troop_slot_ge, "trp_notification_menu_types", ":cur_slot", 1),
          (val_add, ":end_cond", 1),
        (else_try),
          (troop_set_slot, "trp_notification_menu_types", ":cur_slot", ":menu_no"),
          (troop_set_slot, "trp_notification_menu_var1", ":cur_slot", ":menu_var_1"),
          (troop_set_slot, "trp_notification_menu_var2", ":cur_slot", ":menu_var_2"),
        (try_end),
      (try_end),
  ]),
]
