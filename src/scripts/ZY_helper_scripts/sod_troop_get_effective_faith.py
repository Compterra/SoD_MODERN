# COST: O(1)
SCRIPTS = [
("sod_troop_get_effective_faith",
  [
    (assign, ":effective_faith", "$g_sod_global_faith"),
    (store_mul, ":holy_burden", "$g_sod_holy", 10),
    (val_sub, ":effective_faith", ":holy_burden"),
    (assign, reg0, ":effective_faith"),
    (assign, reg1, "$g_sod_global_faith"),
    (assign, reg2, ":holy_burden"),
  ]),
]
