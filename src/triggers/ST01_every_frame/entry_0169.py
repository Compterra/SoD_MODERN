SIMPLE_TRIGGERS = [
(0,
   [
      (try_begin),
        (map_free),
        (eq, "$g_sod_initial_world_setup_pending", 1),
        (party_is_active, "p_main_party"),
        (call_script, "script_sod_finish_initial_party_world_setup"),
      (try_end),
    ]),
]
