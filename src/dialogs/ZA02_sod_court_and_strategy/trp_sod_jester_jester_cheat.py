DIALOGS = [
[trp_sod_jester, "jester_cheat", [
  (this_or_next|eq, "$cheat_mode", 1),
  (eq, "$g_sod_cheat_mode", 1),
], "Item cheat menu.", "jester_cheat1", [

    ]],
[trp_sod_jester, "jester_cheat", [
  (neq, "$cheat_mode", 1),
  (neq, "$g_sod_cheat_mode", 1),
], "That door is closed in this campaign.", "close_window", []],
]
