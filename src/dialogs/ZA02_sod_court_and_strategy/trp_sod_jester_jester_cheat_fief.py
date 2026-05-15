DIALOGS = [
[trp_sod_jester, "jester_cheat_fief", [
  (this_or_next|eq, "$cheat_mode", 1),
  (eq, "$g_sod_cheat_mode", 1),
], "Change fief ownership.", "jester_cheat_fief_choice", []],
[trp_sod_jester, "jester_cheat_fief", [
  (neq, "$cheat_mode", 1),
  (neq, "$g_sod_cheat_mode", 1),
], "That door is closed in this campaign.", "close_window", []],
]
