DIALOGS = [
[trp_sod_jester|plyr|repeat_for_1000, "jester_cheat1",
   [
     (store_repeat_object, ":item_no"),
   (is_between, ":item_no", "itm_sumpter_horse", "itm_items_end"),
     (str_store_item_name, s1, ":item_no")
     ],
   "{s1}", "jester_cheat",
   [(store_repeat_object, "$temp"),
   (troop_add_item, "trp_player", "$temp", 0),
   (val_add, "$g_sod_cheat_mode_used", 1)
   ]
   ],
]
