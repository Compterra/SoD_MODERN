SIMPLE_TRIGGERS = [
(12,
  [
    # we cannot be a prisoner...
    (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 0),
    (party_get_num_companions, ":num_comp", "p_main_party"),
	(gt, ":num_comp", 15),
	
    (store_random_in_range, ":rand" , 0, 200),
	
	(try_begin),
	(eq, "$g_sod_parental_advisory", 0),
	(store_random_in_range, ":event_menu", "mnu_event_04", "mnu_event_holy"),
	(else_try),
    (store_random_in_range, ":event_menu", "mnu_event_04", "mnu_event_04g"),
	(try_end),
	
	(try_begin),
	(eq, "$g_whiped_for_example", 1),
	(lt, ":rand", 5),
	(is_between, ":event_menu", "mnu_event_04f", "mnu_event_04i"),
	(assign, "$g_whiped_for_example", 0),
	(assign, ":event_menu", "mnu_event_22"),
	(else_try),
    (eq, "$g_whiped_for_example", 1),
	(lt, ":rand", 15),
	(is_between, ":event_menu", "mnu_event_04f", "mnu_event_04i"),
	(assign, "$g_whiped_for_example", 0),
	(assign, ":rand", 11), 
	(try_end),
	
	# 7,5% chance to occur

    (lt, ":rand", 15), 
    (jump_to_menu, ":event_menu"),
	
	
  ]),
]
