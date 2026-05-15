DIALOGS = [
[trp_sod_jester|plyr, "jester_cheatc1", [
  (this_or_next|eq, "$cheat_mode", 1),
  (eq, "$g_sod_cheat_mode", 1),
], "ADD CUSTOM RANGED WEAPONS", "jester_else", [
  (try_for_range, ":item_no", "itm_talak_warhammer", "itm_items_end"),
  (item_get_type, ":item_type", ":item_no"),
  (this_or_next|eq, ":item_type", itp_type_arrows),
  (this_or_next|eq, ":item_type", itp_type_bolts),
  (this_or_next|eq, ":item_type", itp_type_bullets),
  (this_or_next|eq, ":item_type", itp_type_thrown),
  (this_or_next|eq, ":item_type", itp_type_bow),
  (this_or_next|eq, ":item_type", itp_type_crossbow),
  (this_or_next|eq, ":item_type", itp_type_pistol),
  (eq, ":item_type", itp_type_musket),
  (troop_add_item, "trp_player", ":item_no", 0),
  (try_end),
  (val_add, "$g_sod_cheat_mode_used", 1)
  ]],
]
