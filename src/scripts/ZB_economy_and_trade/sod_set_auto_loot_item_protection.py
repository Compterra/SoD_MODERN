SCRIPTS = [
("sod_set_auto_loot_item_protection",
 [
   (store_script_param_1, ":item_no"),
   (store_script_param_2, ":protected"),
   (try_begin),
     (gt, ":item_no", 0),
     (val_clamp, ":protected", 0, 2),
     (item_set_slot, ":item_no", slot_item_sod_auto_loot_protected, ":protected"),
   (try_end),
 ]),
]
