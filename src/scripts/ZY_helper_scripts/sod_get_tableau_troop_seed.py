# COST: trivial
SCRIPTS = [
("sod_get_tableau_troop_seed",
  [
    (store_script_param, ":troop_no", 1),

    (try_begin),
      (troop_is_hero, ":troop_no"),
      (assign, ":seed", -1),
    (else_try),
      (store_mul, ":seed", ":troop_no", 126233),
      (val_mod, ":seed", 1000),
      (val_add, ":seed", 1),
    (try_end),

    (assign, reg0, ":seed"),
  ]),
]
