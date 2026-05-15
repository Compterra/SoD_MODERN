DIALOGS = [
[trp_sod_jester|plyr, "jester_cheatc1", [
  (this_or_next|eq, "$cheat_mode", 1),
  (eq, "$g_sod_cheat_mode", 1),
], "ADD CUSTOM MELEE WEAPONS", "jester_else", [
  (try_for_range, ":item_no", "itm_talak_warhammer", "itm_items_end"),
  (item_get_type, ":item_type", ":item_no"),
  (this_or_next|eq, ":item_type", itp_type_one_handed_wpn),
  (this_or_next|eq, ":item_type", itp_type_two_handed_wpn),
  (eq, ":item_type", itp_type_polearm),
  (troop_add_item, "trp_player", ":item_no", 0),
  (try_end),
  (val_add, "$g_sod_cheat_mode_used", 1)
  ]],
]
