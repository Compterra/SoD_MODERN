MENUS = [
(
    "castle_taken", mnf_enable_hot_keys,
    "{s3} has fallen to your troops, and you now have full control of the {reg2?town:castle}.",
    "none",
    [
      (party_clear, "$g_encountered_party"),
      (call_script, "script_lift_siege", "$g_encountered_party", 0),
      (assign, "$g_player_besiege_town", -1),
      (call_script, "script_add_log_entry", logent_castle_captured_by_player, "trp_player", "$g_encountered_party", 0, "$g_encountered_party_faction"),
      (party_set_slot, "$g_encountered_party", slot_center_last_taken_by_troop, "trp_player"),
      #Reduce prosperity of the center by 5
      (call_script, "script_change_center_prosperity", "$g_encountered_party", -5),
      #MORDACHAI - greatly increase the renown value of capturing places
      (try_begin),
        (is_between, "$g_encountered_party", castles_begin, castles_end),
        (call_script, "script_change_troop_renown", "trp_player", 25),
      (else_try),
        (call_script, "script_change_troop_renown", "trp_player", 50),
      (try_end),
      (call_script, "script_add_log_entry", logent_castle_captured_by_player, "trp_player", "$g_encountered_party", -1, "$g_encountered_party_faction"),

      (try_begin),
        # handle the case where the player is a vassal of a kingdom
        (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
        (neq, "$players_kingdom", "fac_player_supporters_faction"),
        (call_script, "script_give_center_to_faction", "$g_encountered_party", "$players_kingdom"),
        (call_script, "script_order_best_besieger_party_to_guard_center", "$g_encountered_party", "$players_kingdom"),
        (jump_to_menu, "mnu_castle_taken_2"),
      (else_try),
        # handle the case where the player is either their own King, or is working for a pretender
        (call_script, "script_give_center_to_faction", "$g_encountered_party", "fac_player_supporters_faction"),
        (call_script, "script_order_best_besieger_party_to_guard_center", "$g_encountered_party", "fac_player_supporters_faction"),
        (str_store_party_name, s3, "$g_encountered_party"),
		
		    (try_begin),                    # Sod Twan Badboy effect
            (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
            (call_script, "script_change_badboy_rating", 10),
            (else_try),
            (call_script, "script_change_badboy_rating", 4),
            (try_end),                       # Twan Badboy effect ends
		
        #MORDACHAI - removed reg1 stuff from here - we don't use it anymore...
      (try_end),

      (assign, reg2, 0),
      (try_begin),
        (is_between, "$g_encountered_party", towns_begin, towns_end),
        (assign, reg2, 1),
      (try_end),
    ],
    [
      ("continue", [], "Continue...",
       [
          (assign, "$auto_enter_town", "$g_encountered_party"),
          (change_screen_return),
        ]),
    ],
  ),
]
