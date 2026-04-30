SCRIPTS = [
("activate_law",
  [
    (store_script_param_1, ":law"),
    (call_script, "script_sod_law_migrate_player_legacy_slots"),
    (call_script, "script_sod_law_add_to_faction", "fac_player_supporters_faction", ":law"),
  ]),
]
