SIMPLE_TRIGGERS = [
(24 * 3, # Every 3 days
    [
      (call_script, "script_sod_trim_bloated_world_parties"),
    ]),
]
