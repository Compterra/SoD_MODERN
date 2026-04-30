DIALOGS = [
[trp_sod_jester|plyr, "jester_cheatc1", [], "ADD NATIVE WEAPONS 1", "jester_else", [
  (try_for_range, ":item_no", "itm_wooden_stick", "itm_mace_1"),
  (troop_add_item, "trp_player", ":item_no", 0),
  (try_end),
  (val_add, "$g_sod_cheat_mode_used", 1)
  ]],
]
