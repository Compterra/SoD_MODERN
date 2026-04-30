MENUS = [
(
    "event_28", mnf_disable_all_keys,
    "Some disciples of the Inner Light visit you. They complain about your calradian subjects love for meat and sausages when people searching enlightnment should only eat vegetables.",
    "none",
    [
    ],
    [
      ("choice_28_1", [], "Force your subjects to only eat vegetables and condemn some known flesh eaters for example.", [
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
         ("choice_28_1", [], "Remind your subjects they should only eat vegetables.", [
	     (val_sub, "$g_sod_global_health", 25),
		 (val_max, "$g_sod_global_health", -100),
		 (val_add, "$g_sod_global_faith", 50),
		 (val_clamp, "$g_sod_global_faith", -2000, 2001),
          (change_screen_return),
        ]
       ),
            ("choice_28_1", [], "Remind your subjects it's better for their health to only eat meat three or for times a week.", [
			 (val_add, "$g_sod_global_health", 20),
			 (val_sub, "$g_sod_clergy_happines", 10),
			 (val_sub, "$g_sod_global_faith", 100),
			 (val_clamp, "$g_sod_global_faith", -2000, 2001),
          (change_screen_return),
        ]
       ),
           ("choice_28_1", [], "Ignore the disciples request.", [
			(val_sub, "$g_sod_clergy_happines", 15),
			(val_sub, "$g_sod_global_faith", 50), 
			(val_clamp, "$g_sod_global_faith", -2000, 2001),
          (change_screen_return),
        ]
       ),
      ]
  ),
]
