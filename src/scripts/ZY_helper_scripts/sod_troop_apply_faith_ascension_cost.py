# COST: O(1)
SCRIPTS = [
("sod_troop_apply_faith_ascension_cost",
  [
    (store_script_param, ":count", 1),

    (val_max, ":count", 0),
    (store_mul, ":holy_cost", ":count", sod_faith_ascension_holy_cost),
    (val_add, "$g_sod_holy", ":holy_cost"),
    (val_clamp, "$g_sod_holy", 0, 10001),
    (assign, reg0, ":holy_cost"),
  ]),
]
