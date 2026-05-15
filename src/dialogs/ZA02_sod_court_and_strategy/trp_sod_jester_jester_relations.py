DIALOGS = [
[trp_sod_jester, "jester_relations", [
  (this_or_next|eq, "$cheat_mode", 1),
  (eq, "$g_sod_cheat_mode", 1),
], "{reg6?Decrease:Increase} by 10 your relations with...", "jester_faction_choice", []],
[trp_sod_jester, "jester_relations", [
  (neq, "$cheat_mode", 1),
  (neq, "$g_sod_cheat_mode", 1),
], "That door is closed in this campaign.", "close_window", []],
]
