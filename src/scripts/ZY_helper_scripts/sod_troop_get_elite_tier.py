# COST: O(1)
SCRIPTS = [
("sod_troop_get_elite_tier",
  [
    (store_script_param, ":troop_no", 1),
    (call_script, "script_sod_troop_get_doctrine", ":troop_no"),
    (assign, reg0, reg1),
  ]),
]
