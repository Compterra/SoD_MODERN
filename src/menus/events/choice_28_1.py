MENUS = [
(
    "event_28", mnf_disable_all_keys,
    "Disciples of the Inner Light visit you. They complain that your Calradian subjects love meat and sausages, while those seeking enlightenment should eat only vegetables.",
    "none",
    [
    ],
    [
      ("choice_28_1", [], "Force your subjects to eat only vegetables and make examples of known meat-eaters.", [
         (val_sub, "$g_sod_global_health", 50),
		 (val_max, "$g_sod_global_health", -100),
		 (val_add, "$g_sod_global_faith", 100),
		 (val_clamp, "$g_sod_global_faith", -2000, 2001),
		 (val_add, "$g_sod_clergy_happines", 10),
		 	   (try_for_range, ":center_no", centers_begin, centers_end),
				(store_faction_of_party, ":center_fac", ":center_no"),
				(eq, ":center_fac", "fac_player_supporters_faction"),
				(neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
					(try_begin),
					 (party_slot_ge, ":center_no", slot_center_sod_local_faith, 0),
					(else_try),
					(call_script, "script_change_player_relation_with_center", ":center_no", 5),
					(try_end),
				(try_end),
      (change_screen_return),
        ]
       ),
         ("choice_28_2", [], "Remind your subjects they should only eat vegetables.", [
	     (val_sub, "$g_sod_global_health", 25),
		 (val_max, "$g_sod_global_health", -100),
		 (val_add, "$g_sod_global_faith", 50),
		 (val_clamp, "$g_sod_global_faith", -2000, 2001),
          (change_screen_return),
        ]
       ),
            ("choice_28_3", [], "Remind your subjects it is better for their health to eat meat only three or four times a week.", [
			 (val_add, "$g_sod_global_health", 20),
			 (val_sub, "$g_sod_clergy_happines", 10),
			 (val_sub, "$g_sod_global_faith", 100),
			 (val_clamp, "$g_sod_global_faith", -2000, 2001),
          (change_screen_return),
        ]
       ),
           ("choice_28_4", [], "Ignore the disciples' request.", [
			(val_sub, "$g_sod_clergy_happines", 15),
			(val_sub, "$g_sod_global_faith", 50), 
			(val_clamp, "$g_sod_global_faith", -2000, 2001),
          (change_screen_return),
        ]
       ),
      ]
  ),
]
