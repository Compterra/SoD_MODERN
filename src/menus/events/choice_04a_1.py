MENUS = [
(
    "event_04a", mnf_disable_all_keys,
    "You encounter the child of one of your soldiers. He explains you that his mother is ill and begs you to release his father from the contract. Harvest was poor and his wages can't feed the whole family. If he could come back and work on the field they might survive.",
    "none",
    [

    ],
    [
      ("choice_04a_1", [], "This can't be! Here take 100 denars.",
       [
       (store_troop_gold, ":gold", "trp_player"),
       (try_begin),
        (ge, ":gold", 100),
        (call_script, "script_change_player_honor", 1),
        (call_script, "script_sod_player_charge_gold", 100),
        (else_try),
        (display_message, "@You don't have enough gold. How embarassing!", quest_fail_color),
        (call_script, "script_change_troop_renown", "trp_player", -5),
        (try_end),
          (change_screen_return),
        ]
       ),

      ("choice_04a_2", [], "Pacta sunt servanda!",
       [(call_script, "script_change_player_honor", -1),
        (change_screen_return),
        ]
       ),

      ("choice_04a_3", [
	  (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),

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
	     (try_end),
	  (try_end),

	  (gt, reg2, 0),
	  (str_store_troop_name, s1, reg2),

	   ], "Let the soldier go (a {s1}).",
       [

       (party_remove_members, "p_main_party", reg2, 1),
       (call_script, "script_change_player_honor", 2),
       (change_screen_return),
        ]
       ),
      ]
  ),
]
