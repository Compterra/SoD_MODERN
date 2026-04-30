# COST: O(1)
SCRIPTS = [
("sod_troop_is_faith_elite",
  [
    (store_script_param, ":troop_no", 1),
    (call_script, "script_sod_troop_get_doctrine", ":troop_no"),
    (assign, ":is_faith", 0),
    (try_begin),
      (this_or_next|eq, reg1, sod_elite_tier_faith),
      (eq, reg0, sod_doctrine_role_faith),
      (assign, ":is_faith", 1),
    (else_try),
      (store_and, ":has_flag", reg3, sod_doctrine_flag_faith),
      (gt, ":has_flag", 0),
      (assign, ":is_faith", 1),
    (try_end),
    (assign, reg0, ":is_faith"),
  ]),
]
