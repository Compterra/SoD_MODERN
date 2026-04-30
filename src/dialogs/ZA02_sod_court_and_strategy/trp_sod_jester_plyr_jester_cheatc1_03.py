DIALOGS = [
[trp_sod_jester|plyr, "jester_cheatc1", [], "ADD ARROWS, GLOVES, BOOTS", "jester_else", [
  (try_for_range, ":item_no", "itm_arrows", "itm_lady_dress_ruby"),
  (troop_add_item, "trp_player", ":item_no", 0),
  (try_end),
  (val_add, "$g_sod_cheat_mode_used", 1)
  ]],
]
