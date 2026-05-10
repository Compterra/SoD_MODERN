MENUS = [
(
    "event_04g", mnf_disable_all_keys,
    "{s2}",
    "none",
    [ (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),

	  (assign, ":num_regular_stacks", 0),
	  (try_for_range, ":stack_no", 1, ":num_stacks"),
	  (party_stack_get_troop_id, ":troop_id", "p_main_party", ":stack_no"),
	  (gt, ":troop_id", 0),
	  (party_stack_get_size, ":size", "p_main_party", ":stack_no"),
	  (neg|troop_is_hero, ":troop_id"),
	  (gt, ":size", 0),
	  (val_add, ":num_regular_stacks", 1),
	  (try_end),

	  (gt, ":num_regular_stacks", 0),
	  (store_add, ":random_upper", ":num_regular_stacks", 1),
	  (store_random_in_range, ":rnd", 1, ":random_upper"),

	  (assign, ":non_hero_stack", 0),
	  (assign, reg2, -1),
	  (assign, ":this_stack", -1),

	  (try_for_range, ":stack_no", 1, ":num_stacks"),
	  (party_stack_get_troop_id, ":troop_id", "p_main_party", ":stack_no"),
	  (gt, ":troop_id", 0),
	  (party_stack_get_size, ":size", "p_main_party", ":stack_no"),
	  (neg|troop_is_hero, ":troop_id"),
	  (gt, ":size", 0),
	  (val_add, ":non_hero_stack", 1),
	     (try_begin),
		 (eq, ":non_hero_stack", ":rnd"),
		 (assign, reg2, ":troop_id"),
		 (assign, ":this_stack", ":stack_no"),
	     (try_end),
	  (try_end),

	  (gt, reg2, 0),
	  (ge, ":this_stack", 0),
	  (party_stack_get_size, ":stack_size", "p_main_party", ":this_stack"),

	  (try_begin),
	     (eq, ":stack_size", 1),
		 (assign, reg3, 1),
	  (else_try),
         (lt, ":stack_size", 4),
         (assign, reg3, ":stack_size"),
      (else_try),
	   	(party_get_morale, ":morale", "p_main_party"),
             (try_begin),
                (lt, ":morale", 30),
                (assign, reg3, ":stack_size"),
             (else_try),
                (lt, ":morale", 60),
                (store_div, reg3, ":stack_size", 2),
 			  (else_try),
			     (store_div, ":max", ":stack_size", 2),
				 (store_random_in_range, reg3, 1, ":max"),
		      (try_end),
        (try_end),

		(str_clear, s2),
        (try_begin),
		(eq, reg3, 1),
	    (str_store_troop_name, s1, reg2),
        (str_store_string, s2, "@One of your soldiers wish to end their contract, a {s1} ask you if they can go home and return to civil life."),
	    (else_try),
        (str_store_troop_name_plural, s1, reg2),
        (str_store_string, s2, "@Some of your soldiers wish to end their contract, {reg3} {s1} ask you if they can go home and return to civil life."),
        (try_end),
    ],
    [
      ("choice_04g_1", [], "You can go home, I'll even give you 50 denars each to help your new start.",
       [
       (store_troop_gold, ":gold", "trp_player"),
	   (store_mul, ":cost", reg3, 50),
       (try_begin),
        (ge, ":gold", ":cost"),
		(assign, ":honor_gain", reg3),
		(val_clamp, ":honor_gain", 3, 6),
        (call_script, "script_change_player_honor", ":honor_gain"),
        (call_script, "script_sod_player_charge_gold", ":cost"),
	    (call_script, "script_change_player_party_morale", 10),
        (else_try),
        (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
        (try_end),
		(party_remove_members, "p_main_party", reg2, reg3),
          (change_screen_return),
        ]
       ),

      ("choice_04g_2", [], "You can go home.",
       [
	   	(call_script, "script_change_player_party_morale", 5),
	     (party_remove_members, "p_main_party", reg2, reg3),
		 (call_script, "script_change_player_honor", 2),
        (change_screen_return),
        ]
       ),

      ("choice_04g_3", [], "Pay me 50 denars each for ending your contract, and I'll allow you to go home.",
       [
       (party_remove_members, "p_main_party", reg2, reg3),
       (store_mul, ":gold_gain", reg3, 50),
       (troop_add_gold, "trp_player", ":gold_gain"),
       (change_screen_return),
        ]
       ),

	  ("choice_04g_4", [], "I refuse.",
       [
	   	(call_script, "script_change_player_party_morale", -5),
		 (call_script, "script_change_player_honor", -1),
       (change_screen_return),
        ]
       ),

	  ("choice_04g_5", [  ], "You will be whiped for asking this !",
       [
        (call_script, "script_change_player_party_morale", -15),
		(call_script, "script_change_player_honor", -2),
		(assign, "$g_whiped_for_example", 1),
       (change_screen_return),
        ]
       ),

      ]
  ),
]
