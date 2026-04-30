SCRIPTS = [
("npc_get_troop_wage",
    [
      (store_script_param_1, ":troop_id"),
      (assign, ":wage", 0),
      (try_begin),
        (troop_is_hero, ":troop_id"),
      (else_try),
        (store_character_level, ":wage", ":troop_id"),
        (val_mul, ":wage", ":wage"),
        (val_add, ":wage", 50),
        (val_div, ":wage", 30),
        (troop_is_mounted, ":troop_id"),
        (val_mul, ":wage", 5),
        (val_div, ":wage", 4),
      (try_end),
      (assign, reg0, ":wage"),
  ]),
]
