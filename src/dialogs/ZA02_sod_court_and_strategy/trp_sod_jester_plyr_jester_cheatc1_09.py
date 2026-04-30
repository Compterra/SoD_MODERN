DIALOGS = [
[trp_sod_jester|plyr, "jester_cheatc1", [], "ADD RANGEF", "jester_else", [
  (try_for_range, ":item_no", "itm_jarid", "itm_talak_warhammer"),
  (troop_add_item, "trp_player", ":item_no", 0),
  (try_end),
  (val_add, "$g_sod_cheat_mode_used", 1)
  ]],
]
