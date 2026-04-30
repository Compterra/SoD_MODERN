SCRIPTS = [
("sod_get_cost_to_upgrade_troop_at",
  [
    (store_script_param, ":upgrade", 1),
    (store_script_param, ":center", 2),
    (call_script, "script_sod_troop_get_upgrade_cost", ":upgrade", ":center"),
  ]),
]
