SIMPLE_TRIGGERS = [
(20,
  [
    # can't be a prisoner
    (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 0),

    # must be a king
    (eq, "$g_sod_king", 1),

	# must have a temple
	
	(assign, ":num_temples", 0),
	
	(try_for_range, ":center_no", towns_begin, towns_end),
	(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
	  (try_begin),
      (party_slot_eq, ":center_no", slot_center_has_temple, 1),
	  (val_add, ":num_temples", 1),
	  (try_end),
	(try_end),
	
    # 1% chance per temple for a randome event to occur 
    (store_random_in_range, ":rand" , 0, 100),
    (lt, ":rand", ":num_temples"),

    # do one of the following events...
        (try_begin),
            (eq, "$g_sod_faith", cb_the_one),
            (assign, ":event_one", "mnu_event_23"),
            (assign, ":event_two", "mnu_event_24"),  
            (assign, ":event_three", "mnu_event_25"),			
          (else_try),
            (eq, "$g_sod_faith", cb_old_gods),
            (assign, ":event_one", "mnu_event_25"),
			(assign, ":event_two", "mnu_event_26"),
			(assign, ":event_three", "mnu_event_27"),
          (else_try),
            (eq, "$g_sod_faith", cb_the_void),
            (assign, ":event_one", "mnu_event_27"),
			(assign, ":event_two", "mnu_event_26"),
			(assign, ":event_three", "mnu_event_25"),
          (else_try),
            (eq, "$g_sod_faith", cb_enlightenment),
            (assign, ":event_one", "mnu_event_24"),
            (assign, ":event_two", "mnu_event_28"),
            (assign, ":event_three", "mnu_event_30"),			
          (else_try),
            (eq, "$g_sod_faith", cb_atheism),
            (assign, ":event_one", "mnu_event_29"),
			(assign, ":event_two", "mnu_event_24"),
			(assign, ":event_three", "mnu_event_25"),
          (try_end),
		  
		  (store_random_in_range, ":rand2", 0, 100),
		  (try_begin),
		  (lt, ":rand2", 40),
		  (jump_to_menu, ":event_one"),
          (else_try),
		  (lt, ":rand2", 75),
          (jump_to_menu, ":event_two"),
		  (else_try),
		  (jump_to_menu, ":event_three"),
          (try_end),  		  
		  
  ]),
]
