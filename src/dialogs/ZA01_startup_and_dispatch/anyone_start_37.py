DIALOGS = [
[anyone, "start", [
  (eq, "$talk_context", tc_mercenary_base),
  (call_script, "script_get_random_string_for_troop", s1, "$g_talk_troop"),
  ], "{s1}", "close_window", []],
]
