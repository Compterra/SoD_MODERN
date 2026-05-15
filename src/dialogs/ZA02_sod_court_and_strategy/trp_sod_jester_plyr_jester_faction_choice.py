DIALOGS = [
[trp_sod_jester|plyr, "jester_faction_choice", [
  (this_or_next|eq, "$cheat_mode", 1),
  (eq, "$g_sod_cheat_mode", 1),
  (eq, reg6, 0),
], "Decrease relations instead.", "jester_relations", [(assign, reg6, 1)]],
]
