MENUS = [
(
    "event_23", mnf_disable_all_keys,
    "Some priests of the One visit you. They complain about town merchants who loan money to farmers and take interests when earning money with bank operations is clearly forbidden by the sacred texts.\
They think that seizing the benefits of these greedy moneylenders and distributing it to the poor peasants, would help your religion to spread.",
    "none",
    [
    ],
    [
      ("choice_23_1", [], "Do as they want (will reduce both your town relations and prosperity).", [
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
      ("choice_23_2", [], "Do as they want, but with exceptions for influent merchants.", [
	  
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
           ("choice_23_3", [], "Seize moneylenders money, but keep it for you.", [
			 
		   (try_for_range, ":town_no", towns_begin, towns_end),
		   (party_slot_eq, ":town_no", slot_town_lord, "trp_player"),
		   (call_script, "script_change_center_prosperity", ":town_no", -5),
		   (call_script, "script_change_player_relation_with_center", ":town_no", -5),
		   (try_end),
	       
		   (val_sub, "$g_sod_global_faith", 100),
		   (val_clamp, "$g_sod_global_faith", -2000, 2001),
		   (val_clamp, "$g_sod_global_faith", -2000, 2001),
		   (val_sub, "$g_sod_clergy_happines", 5),
		   
		   (call_script, "script_change_player_honor", -5),
		   (store_random_in_range, ":gold", 1000, 3000),
		   (troop_add_gold, "trp_player", ":gold"),
          (change_screen_return),
        ]
       ),
      ("choice_23_4", [], "Refuse the priests proposal (bankers will pay you 1000 denars for that).", [
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
