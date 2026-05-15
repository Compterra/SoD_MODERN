DIALOGS = [
[trp_sod_jester, "jester_cheatc", [
  (this_or_next|eq, "$cheat_mode", 1),
  (eq, "$g_sod_cheat_mode", 1),
], "Item category cheat menu.", "jester_cheatc1", [

    ]],
[trp_sod_jester, "jester_cheatc", [
  (neq, "$cheat_mode", 1),
  (neq, "$g_sod_cheat_mode", 1),
], "That door is closed in this campaign.", "close_window", []],
]
