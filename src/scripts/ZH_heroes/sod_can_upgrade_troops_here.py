SCRIPTS = [
("sod_can_upgrade_troops_here",
  [
    (store_script_param, ":upgrade", 1),
    (store_script_param, ":center_no", 2),
    (call_script, "script_sod_troop_can_upgrade_at_center", ":upgrade", ":center_no"),
  ]),
]
