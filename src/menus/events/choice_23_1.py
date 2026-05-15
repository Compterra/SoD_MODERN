MENUS = [
(
    "event_23", mnf_disable_all_keys,
    "Priests of the One visit you. They accuse town moneylenders of charging farmers interest, a practice forbidden by their sacred texts. They say seizing the lenders' profits and giving them to poor peasants would help the faith spread.",
    "none",
    [
    ],
    [
      ("choice_23_1", [], "Seize the lenders' profits and give them to the poor.", [
	       (try_for_range, ":town_no", towns_begin, towns_end),
		   (party_slot_eq, ":town_no", slot_town_lord, "trp_player"),
		   (call_script, "script_change_center_prosperity", ":town_no", -5),
		   (call_script, "script_change_player_relation_with_center", ":town_no", -5),
		   (try_end),
		   
		   (try_for_range, ":village_no", villages_begin, villages_end),
		   (party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
		   (call_script, "script_change_player_relation_with_center", ":village_no", 3),
		   (try_end),
	       
		   (val_add, "$g_sod_global_faith", 100),
		   (val_clamp, "$g_sod_global_faith", -2000, 2001),
	       (val_add, "$g_sod_clergy_happines", 10),
	  
          (change_screen_return),
        ]
       ),
      ("choice_23_2", [], "Seize the worst offenders' profits, but spare influential merchants.", [
	  
	  	   (try_for_range, ":town_no", towns_begin, towns_end),
		   (party_slot_eq, ":town_no", slot_town_lord, "trp_player"),
		   (call_script, "script_change_center_prosperity", ":town_no", -3),
		   (try_end),
		   
		   (try_for_range, ":village_no", villages_begin, villages_end),
		   (party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
		   (call_script, "script_change_player_relation_with_center", ":village_no", 2),
		   (try_end),
	       
		   (val_add, "$g_sod_clergy_happines", 5),
		   (val_add, "$g_sod_global_faith", 50),
		   (val_clamp, "$g_sod_global_faith", -2000, 2001),
	  
          (change_screen_return),
        ]
       ),
           ("choice_23_3", [], "Seize the moneylenders' wealth and keep it for yourself.", [
			 
		   (try_for_range, ":town_no", towns_begin, towns_end),
		   (party_slot_eq, ":town_no", slot_town_lord, "trp_player"),
		   (call_script, "script_change_center_prosperity", ":town_no", -5),
		   (call_script, "script_change_player_relation_with_center", ":town_no", -5),
		   (try_end),
	       
		   (val_sub, "$g_sod_global_faith", 100),
		   (val_clamp, "$g_sod_global_faith", -2000, 2001),
		   (val_sub, "$g_sod_clergy_happines", 5),
		   
		   (call_script, "script_change_player_honor", -5),
		   (store_random_in_range, ":gold", 1000, 3000),
		   (troop_add_gold, "trp_player", ":gold"),
          (change_screen_return),
        ]
       ),
      ("choice_23_4", [], "Refuse the priests. The bankers will pay 1000 denars for protection.", [
		(troop_add_gold, "trp_player", 1000),
    	(val_sub, "$g_sod_global_faith", 50),
    	(val_clamp, "$g_sod_global_faith", -2000, 2001),
	  	(val_sub, "$g_sod_clergy_happines", 20),
	  
          (change_screen_return),
        ]
       ),
      ]
  ),
]
