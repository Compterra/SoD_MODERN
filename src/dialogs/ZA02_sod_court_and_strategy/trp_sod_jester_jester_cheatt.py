DIALOGS = [
[trp_sod_jester, "jester_cheatt", [
  (this_or_next|eq, "$cheat_mode", 1),
  (eq, "$g_sod_cheat_mode", 1),
], "Troop cheat menu.", "jester_cheatt1", [

    ]],
[trp_sod_jester, "jester_cheatt", [
  (neq, "$cheat_mode", 1),
  (neq, "$g_sod_cheat_mode", 1),
], "That door is closed in this campaign.", "close_window", []],
]
