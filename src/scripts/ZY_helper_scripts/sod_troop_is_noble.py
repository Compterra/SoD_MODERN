# COST: O(1)
SCRIPTS = [
("sod_troop_is_noble",
  [
    (store_script_param, ":troop_no", 1),
    (call_script, "script_sod_troop_get_doctrine", ":troop_no"),
    (assign, ":is_noble", 0),
    (try_begin),
      (this_or_next|eq, reg1, sod_elite_tier_noble),
      (eq, reg1, sod_elite_tier_faith),
      (assign, ":is_noble", 1),
    (else_try),
      (store_and, ":has_flag", reg3, sod_doctrine_flag_noble),
      (gt, ":has_flag", 0),
      (assign, ":is_noble", 1),
    (try_end),
    (assign, reg0, ":is_noble"),
  ]),
]
