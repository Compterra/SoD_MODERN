MENUS = [
(
    "event_30", mnf_disable_all_keys,
    "Disciples of the Inner Light visit you. They complain that your Calradian subjects drink too much wine and beer, and urge you to restrict alcohol throughout the realm.",
    "none",
    [
    ],
   [   ("choice_30_1", [], "Prohibit alcohol and punish a few known drunkards as examples.", [
         (val_add, "$g_sod_global_health", 20),
		 (val_min, "$g_sod_global_health", 100),
		 (val_add, "$g_sod_global_faith", 100),
		 (val_clamp, "$g_sod_global_faith", -2000, 2001),
		 (val_add, "$g_sod_clergy_happines", 10),
		 	   (try_for_range, ":center_no", centers_begin, centers_end),
				(store_faction_of_party, ":center_fac", ":center_no"),
				(eq, ":center_fac", "fac_player_supporters_faction"),
				(neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
					(try_begin),
					 (party_slot_ge, ":center_no", slot_center_sod_local_faith, 25),
					(else_try),
					(call_script, "script_change_player_relation_with_center", ":center_no", -10),
					(try_end),
					(try_begin),
					(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
					(party_slot_eq, ":center_no", slot_center_has_inn, 1),
					(call_script, "script_change_center_prosperity", ":center_no", -5),
					(try_end),
				(try_end),

				
      (change_screen_return),
        ]
       ),
         ("choice_30_2", [], "Warn your subjects that drink harms body and soul.", [
	     (val_add, "$g_sod_global_health", 5),
		 (val_min, "$g_sod_global_health", 100),
		 (val_add, "$g_sod_global_faith", 50),
		 (val_clamp, "$g_sod_global_faith", -2000, 2001),
		 		(try_for_range, ":center_no", centers_begin, centers_end),
				(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
				(neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
					(try_begin),
					 (party_slot_ge, ":center_no", slot_center_sod_local_faith, 0),
					(else_try),
					(call_script, "script_change_player_relation_with_center", ":center_no", -5),
					(try_end),
					(try_begin),
					(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
					(party_slot_eq, ":center_no", slot_center_has_inn, 1),
					(call_script, "script_change_center_prosperity", ":center_no", -3),
					(try_end),
				(try_end),
          (change_screen_return),
        ]
       ),
	   
           ("choice_30_3", [], "Ignore the disciples' request.", [
			(val_sub, "$g_sod_clergy_happines", 15),
			(val_sub, "$g_sod_global_faith", 100), 
			(val_clamp, "$g_sod_global_faith", -2000, 2001),
          (change_screen_return),
        ]
       ),
      ]
  ),
]
