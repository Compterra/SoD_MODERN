MENUS = [
(
    "question_peace_offer", 0,     # SoD Twan adapted the text to the new system, s3 give some explanations for the ai decision
    "You Receive a Peace Offer from {s1}^^{s31}^They propose a truce untill {s4}^^ What is your answer?",
    "none",
    [
      (str_store_faction_name, s1, "$g_notification_menu_var1"),
      (set_fixed_point_multiplier, 100),
      (position_set_x, pos0, 65),
      (position_set_y, pos0, 30),
      (position_set_z, pos0, 170),
      (set_game_menu_tableau_mesh, "tableau_faction_note_mesh_banner", "$g_notification_menu_var1", pos0),
      (store_current_day, ":truce_day"),
      (val_add, ":truce_day", 31),
      (str_store_date, s4, ":truce_day"),  # Sod Twan changes end
      ],
    [
      ("peace_offer_accept", [], "Accept",
       [                                                    
         (call_script, "script_diplomacy_start_peace_between_kingdoms", "fac_player_supporters_faction", "$g_notification_menu_var1", 1),
         (call_script, "script_change_badboy_rating", -2),
		 (change_screen_return),
        ]),
      ("peace_offer_reject", [], "Reject",
       [   (assign, reg0, -1), 
         (call_script, "script_change_player_relation_with_faction", "$g_notification_menu_var1", -5),
		 (call_script, "script_change_badboy_rating", 2),
         (change_screen_return),  
        ]),
     ]
  ),
]
