MENUS = [
(
    "event_24", mnf_disable_all_keys,
    "Some {s2} visit you. They complain about your lack of humility, arguing that a modest ruler would help the faith spread.",
    "none",
    [  (try_begin),
	    (eq, "$g_sod_faith", cb_the_one),
		(str_store_string, s2, "@priests of the One"),
		(else_try),
		(eq, "$g_sod_faith", cb_enlightenment),
		(str_store_string, s2, "@disciples of the Inner Light"),
		(else_try),
		(str_store_string, s2, "@philosophers"),
		(try_end),
		(troop_get_slot, reg0, "trp_player", slot_troop_renown),
		(val_div, reg0, 15),
		(store_div, reg1, reg0, 2),
    ],
    [
      ("choice_24_1", [], "Do as they want (cost: {reg0} renown).", [
	      (val_mul, reg0, -1),
		  (call_script, "script_change_troop_renown", "trp_player", reg0),
		  (call_script, "script_change_player_honor", 2),
		  (val_add, "$g_sod_global_faith", 100),
		  (val_clamp, "$g_sod_global_faith", -2000, 2001),
	      (val_add, "$g_sod_clergy_happines", 10),
          (change_screen_return),
        ]
       ),
             ("choice_24_2", [], "Show a little more humility.", [
			 (val_mul, reg1, -1),
			(call_script, "script_change_troop_renown", "trp_player", reg1),
		    (val_add, "$g_sod_global_faith", 50),
		    (val_clamp, "$g_sod_global_faith", -2000, 2001),
	        (val_add, "$g_sod_clergy_happines", 5),
          (change_screen_return),
        ]
       ),
             ("choice_24_3", [], "Refuse. Majesty does not bow to humility.", [
		  (val_sub, "$g_sod_clergy_happines", 10),
		  (val_sub, "$g_sod_global_faith", 25),
		  (val_clamp, "$g_sod_global_faith", -2000, 2001),
          (change_screen_return),
        ]
       ),
            ("choice_24_4", [], "Condemn them for insulting your majesty and seize their goods.", [
		   (val_sub, "$g_sod_global_faith", 100),
		   (val_clamp, "$g_sod_global_faith", -2000, 2001),
		   
		   (call_script, "script_change_player_honor", -5),
		   (store_random_in_range, ":gold", 200, 500),
		   (troop_add_gold, "trp_player", ":gold"),
			 
          (change_screen_return),
        ]
       ),
      ]
  ),
]
