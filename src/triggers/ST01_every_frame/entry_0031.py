SIMPLE_TRIGGERS = [
(0,
   [
   (eq, "$g_recalculate_ais", 1),
   (assign, "$g_recalculate_ais", 0),
   (call_script, "script_recalculate_ais"),
    ]),
]
