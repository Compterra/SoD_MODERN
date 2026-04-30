SCRIPTS = [
("cf_troop_check_troop_is_enemy",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":checked_troop_no"),
      (assign, ":result", 0),
      (try_for_range, ":i_enemy_slot", slot_troop_enemies_begin, slot_troop_enemies_end),
        (troop_slot_eq, ":troop_no", ":i_enemy_slot", ":checked_troop_no"),
        (assign, ":result", 1),
      (try_end),
      (eq, ":result", 1),
  ]),
]
