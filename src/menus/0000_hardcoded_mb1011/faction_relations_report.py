MENUS = [
("faction_relations_report", mnf_enable_hot_keys,
   "{s1}",
   "none",
   [
    (set_background_mesh, "mesh_pic_report_screen"),
    (str_clear, s2),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      (neq, ":cur_kingdom", "fac_player_supporters_faction"),
      (store_relation, ":cur_relation", "fac_player_supporters_faction", ":cur_kingdom"),
      (call_script, "script_get_realtion_name_s3", ":cur_relation"),
      (str_store_faction_name, s4, ":cur_kingdom"),
      (str_store_string, s2, "@{s2}^{s4}: {s3}"),
    (try_end),
	
	(str_clear, s5), # SoD Twan display truces
    (store_current_day, ":cur_day"),
		(try_for_range, ":slot_no", faction_truce_slots_begin, faction_truce_slots_end),                                 
		(faction_get_slot, ":truce_day", "fac_player_supporters_faction", ":slot_no"),
		(try_begin),
		(gt, ":truce_day", ":cur_day"),
		(store_sub, ":truce_days_remaining", ":truce_day", ":cur_day"),
		(store_sub, ":kingdom_no", ":slot_no", faction_truce_slots_begin),
		(val_add, ":kingdom_no", "fac_player_supporters_faction"),
		(str_store_faction_name, s6, ":kingdom_no"),
    (try_begin),
      (lt, ":truce_days_remaining", 7),
      (str_store_string, s7, "@nearly expired"),
    (else_try),
      (lt, ":truce_days_remaining", 21),
      (str_store_string, s7, "@still recent"),
    (else_try),
      (str_store_string, s7, "@secure for now"),
    (try_end),
		(str_store_string, s5, "@{s5}You have a peace agreement with {s6}; it is {s7}.^"),
		(try_end),
		(try_end),
    (str_store_string, s1, "@Your relation with the factions are:^{s2}^^{s5}"),                           # SoD twan end
    ],
    [
      ("continue", [], "Continue...",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  ),
]
