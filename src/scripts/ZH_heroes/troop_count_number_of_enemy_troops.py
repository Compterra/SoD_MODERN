SCRIPTS = [
("troop_count_number_of_enemy_troops",
    [
      (store_script_param_1, ":troop_no"),
      (assign, ":enemy_count", 0),
      (try_for_range, ":i_enemy_slot", slot_troop_enemies_begin, slot_troop_enemies_end),
        (troop_slot_ge, ":troop_no", ":i_enemy_slot", 1),
        (val_add, ":enemy_count", 1),
      (try_end),
      (assign, reg0, ":enemy_count"),
  ]),
]
