SIMPLE_TRIGGERS = [
(36,
    [
      (call_script, "script_spawn_bandits"),
	  (eq, "$g_sod_debug", 1),
		(display_message, "@Bandits spawned.", debug_color),
    ]),
]
