DIALOGS = [
[trp_sod_jester, "start", [
  (this_or_next|eq, "$cheat_mode", 1),
  (eq, "$g_sod_cheat_mode", 1),
  (eq, "$g_jester_me", 1),
  ], "Welcome not-You. It's not-Me.", "jester_talk", []],
]
