DIALOGS = [
[trp_sod_jester|plyr, "jester_cheatc1", [
  (this_or_next|eq, "$cheat_mode", 1),
  (eq, "$g_sod_cheat_mode", 1),
], "ADD SHIELDS", "jester_else", [
  (try_for_range, ":item_no", shields_begin, shields_end),
  (troop_add_item, "trp_player", ":item_no", 0),
  (try_end),
  (val_add, "$g_sod_cheat_mode_used", 1)
  ]],
]
