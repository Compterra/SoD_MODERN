DIALOGS = [
[trp_sod_jester|plyr, "jester_cheatc1", [
  (this_or_next|eq, "$cheat_mode", 1),
  (eq, "$g_sod_cheat_mode", 1),
], "CLEAR INVENTORY", "jester_else", [
  (troop_clear_inventory, "trp_player"),
  (val_add, "$g_sod_cheat_mode_used", 1),
  ]],
]
