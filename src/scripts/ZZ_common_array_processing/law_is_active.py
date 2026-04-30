SCRIPTS = [
("law_is_active",
  [
    (store_script_param_1, ":law"),
    (call_script, "script_sod_law_is_active_for_faction", "fac_player_supporters_faction", ":law"),
  ]),
]
