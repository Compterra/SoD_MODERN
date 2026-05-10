SIMPLE_TRIGGERS = [
(24 * 7,
  [
    (try_for_range, ":center_no", centers_begin, centers_end),
      (call_script, "script_sod_apply_weekly_faith_drift", ":center_no"),
    (try_end),
    (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
      (call_script, "script_sod_get_realm_faith_profile", ":faction_no"),
    (try_end),
    (call_script, "script_sod_get_realm_faith_profile", "fac_player_supporters_faction"),
  ]),
]
