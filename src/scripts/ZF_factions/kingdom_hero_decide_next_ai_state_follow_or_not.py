SCRIPTS = [
("kingdom_hero_decide_next_ai_state_follow_or_not",
    [
      (store_script_param_1, ":troop_no"),
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),

      (try_begin), #tr1
        (party_get_slot, ":old_ai_state", ":party_no", slot_party_ai_state),
		
        (assign, ":cancel", 0),
        (try_begin), #tr2 if we are retreating to a center keep retreating
          (eq, ":old_ai_state", spai_retreating_to_center),
          (neg|party_is_in_any_town, ":party_no"),
          (assign, ":cancel", 1),          #twan453 removed the ai state if lord is in town change may have created problem with recent war declaration		
          (else_try),
          (troop_slot_eq, ":troop_no", slot_lord_initiative, -10), #twan453 lords ordered to hold center 
          (assign, ":cancel", 1),  		  
        (try_end), #end tr2
		
        (eq, ":cancel", 0),

        (party_get_slot, ":our_strength", ":party_no", slot_party_cached_strength),
		
		(store_troop_faction, ":faction_no", ":troop_no"),  # twan begin
		
        (try_begin), #tr3
		(try_begin),
		(gt, ":our_strength", 0),
		(store_div, ":min_strength_behind", ":our_strength", 2),
		(else_try),
		(assign, ":min_strength_behind", 0),
		(try_end),
        (try_end), # end tr3 twan new
		
        (assign, ":under_siege", 0),
        #find current center
        (party_get_attached_to, ":cur_center_no", ":party_no"),
        (try_begin), #tr4
          (lt, ":cur_center_no", 0),
          (party_get_cur_town, ":cur_center_no", ":party_no"),
        (try_end), #end tr4
        (try_begin), #tr5
          (neg|is_between, ":cur_center_no", walled_centers_begin, walled_centers_end), #twan new
          (assign, ":cur_center_no", -1),
          (assign, ":cur_center_nearby_strength", 0),
          (assign, ":cur_center_left_strength", 1000000), #must be higher than our strength
		  (assign, ":my_center_threat_level", 0), 
        (else_try),
          (party_get_slot, ":cur_center_nearby_strength", ":cur_center_no", slot_party_nearby_friend_strength),
		  (try_begin), #tr6
			  (eq, "$g_sod_deactivate_ai", 0),  # sod twan new
			  (call_script, "script_party_calculate_siege_or_not_strength", ":party_no", 1),
			  (assign, ":siege_strength", reg0),
			  (party_get_slot, ":center_cached_str", ":cur_center_no", slot_party_cached_strength),
			  (val_add, ":cur_center_nearby_strength", ":center_cached_str"),
			  (call_script, "script_get_center_threat_level", ":cur_center_no"), # twan new
			  (assign, ":my_center_threat_level", reg0),
			  (try_begin),
			  (gt, "$g_average_lord_army_strength", 0),
			  (store_div, ":min_strength_unit", "$g_average_lord_army_strength", 20),
			  (else_try),
			  (assign, ":min_strength_unit", 0),
			  (try_end),
			  (faction_get_slot, ":ambition", ":faction_no", slot_faction_ambition),
			  (store_add, ":optimism", ":ambition", 40),
			  (store_mul, ":min_strength_behind", ":min_strength_unit", ":optimism"),  #twan453	
				  (try_begin), #tr7
				  (party_slot_eq, ":cur_center_no", slot_party_type, spt_town),
				  (val_mul, ":min_strength_behind", 3),
				  (val_div, ":min_strength_behind", 2),
				  (try_end), 		#tr7
			  (store_sub, ":cur_center_left_strength", ":cur_center_nearby_strength", ":siege_strength"),			  
			  (else_try),                     
			  (store_sub, ":cur_center_left_strength", ":cur_center_nearby_strength", ":our_strength"),
			  (assign, ":my_center_threat_level", 0),
          (try_end), 
   
          (try_begin), #tr5b 
          (party_get_slot, ":besieger_party", ":cur_center_no", slot_center_is_besieged_by),
          (gt, ":besieger_party", 0),
          (party_is_active, ":besieger_party"),
          (assign, ":under_siege", 1),
		  (try_end), #tr5b
        (try_end), #end tr5

        (faction_get_slot, ":faction_ai_state",  ":faction_no", slot_faction_ai_state),

        (party_get_slot, ":commander_party", ":party_no", slot_party_commander_party),
        (try_begin), #tr8
          (ge, ":commander_party", 0),
          (try_begin), #tr9
            (assign, ":valid_commander_party", 0),
            (try_begin),
              (eq, ":commander_party", "p_main_party"),
              (eq, ":faction_no", "$players_kingdom"),
              (assign, ":valid_commander_party", 1),
            (else_try),
              (gt, ":commander_party", 0),
              (party_is_active, ":commander_party"),
              (assign, ":valid_commander_party", 1),
            (try_end),
            (eq, ":valid_commander_party", 1),
            (try_begin), #tr10
              (store_faction_of_party, ":commander_faction", ":commander_party"),
              (neq, ":faction_no", ":commander_faction"),
              (assign, ":continue", 0),
              (try_begin), #tr11
                (neq, ":commander_party", "p_main_party"),
                (assign, ":continue", 1),
              (else_try),
                (neq, "$players_kingdom", ":faction_no"),
                (assign, ":continue", 1),
              (try_end), #end tr11
              (eq, ":continue", 1),
              (assign, ":commander_party", -1),
            (try_end), #end tr10
          (else_try),
            (assign, ":commander_party", -1),
          (try_end), #end tr9
        (try_end), #end tr8

        (faction_get_slot, ":num_towns", ":faction_no", slot_faction_num_towns),
        (store_mul, ":faction_center_value", ":num_towns", 2),
        (faction_get_slot, ":num_castles", ":faction_no", slot_faction_num_castles),
        (val_add, ":faction_center_value", ":num_castles"),
        (val_mul, ":faction_center_value", 10),
        (val_max, ":faction_center_value", 5),

        (troop_get_slot, ":readiness", ":troop_no", slot_troop_readiness_to_join_army),
        (assign, ":chance_to_follow_other_party", 0),
        (assign, ":target_to_follow_other_party", -1),

        (try_begin), #tr12 follow other party
          (eq, ":under_siege", 0),
          (ge, ":cur_center_left_strength", ":min_strength_behind"),
          (assign, ":continue", 0),
          (try_begin), #tr13
            (ge, ":commander_party", 0),
            (gt, "$party_relative_strength", 30),
            (assign, ":continue", 1),
          (else_try),
            (gt, "$party_relative_strength", 50),
            (lt, "$ratio_of_prisoners", 50),
            (assign, ":continue", 1),
          (try_end), #end tr13
          (eq, ":continue", 1),
          (try_begin), #tr14
            (eq, ":faction_no", "fac_player_supporters_faction"),
            (neg|troop_slot_eq, ":troop_no", slot_troop_player_order_state, spai_undefined),
            (assign, ":continue", 0),
          (try_end), #end tr14
          (eq, ":continue", 1),
          (faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
          (ge, ":faction_marshall", 0),
          #(troop_slot_eq, ":faction_marshall", slot_troop_is_prisoner, 0),
          (neg|troop_slot_ge, ":faction_marshall", slot_troop_prisoner_of_party, 0),
          (troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
          (neq, ":faction_marshall", ":troop_no"),
          (gt, ":faction_marshall_party", 0),
          (party_is_active, ":faction_marshall_party"),


          (try_begin), #tr15
            (eq, ":faction_ai_state", sfai_gathering_army),
            (assign, ":old_target_to_follow_other_party", -1),
            (try_begin), #tr16
              (ge, ":commander_party", 0),
              (assign, ":old_target_to_follow_other_party", ":commander_party"),
            (try_end), #end tr16

            (assign, ":continue", 0),
            (try_begin), #tr17
              (ge, ":readiness", 60),
              (assign, ":continue", 1),
            (else_try),
              (ge, ":readiness", 10),
              (eq, ":old_target_to_follow_other_party", ":faction_marshall_party"),
              (assign, ":continue", 1),
            (try_end), #end tr17

            (try_begin), #tr18
              (eq, ":continue", 1),
              (store_distance_to_party_from_party, ":dist", ":faction_marshall_party", ":party_no"),
              (store_sub, ":chance", 120, ":dist"),
              ##            (val_mul, ":chance", 3),
              ##            (val_div, ":chance", 2),
              (val_min, ":chance", 100),
              (val_max, ":chance", 20),
              (store_sub, ":faction_advantage_effect", "$g_average_center_value_per_faction", ":faction_center_value"),
              (val_mul, ":faction_advantage_effect", 2),
              (val_add, ":chance", ":faction_advantage_effect"),
              (val_max, ":chance", 10),

              (assign, ":target_to_follow_other_party", ":faction_marshall_party"),
              (assign, ":chance_to_follow_other_party", ":chance"),
              (try_begin), #tr19
                (eq, ":old_target_to_follow_other_party", ":target_to_follow_other_party"),
                (val_mul, ":chance_to_follow_other_party", 1000),
              (try_end), #end tr19
            (try_end), #end tr18
          (else_try),
            (this_or_next|eq, ":faction_ai_state", sfai_attacking_center),
            (this_or_next|eq, ":faction_ai_state", sfai_raiding_village),
            (this_or_next|eq, ":faction_ai_state", sfai_attacking_enemies_around_center),
            (eq, ":faction_ai_state", sfai_attacking_enemy_army),
            (eq, ":commander_party", ":faction_marshall_party"),
            (ge, ":readiness", 10),
            (assign, ":target_to_follow_other_party", ":faction_marshall_party"),
            (assign, ":chance_to_follow_other_party", 100000),
          (try_end), #end tr15
        (try_end), #end tr12
		
        (try_begin), #tr16 follow other party with initiative
          (le, ":chance_to_follow_other_party", 0),
          (eq, ":under_siege", 0),
          (ge, ":cur_center_left_strength", ":min_strength_behind"),
          (assign, ":continue", 0),
          (try_begin),#tr17
            (ge, ":commander_party", 0),
            (gt, "$party_relative_strength", 40),
            (assign, ":continue", 1),
          (else_try),
            (gt, "$party_relative_strength", 75),
            (lt, "$ratio_of_prisoners", 50),
            (assign, ":continue", 1),
          (try_end), #end tr17
          (eq, ":continue", 1),
          (try_begin), #tr18
            (eq, ":faction_no", "fac_player_supporters_faction"),
            (neg|troop_slot_eq, ":troop_no", slot_troop_player_order_state, spai_undefined),
            (neg|troop_slot_eq, ":troop_no", slot_troop_player_order_state, spai_accompanying_army),
            (assign, ":continue", 0),
          (try_end), #end tr18
          (eq, ":continue", 1),
          (neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),

          (assign, ":old_target_to_follow_other_party", -1),
          (try_begin), #tr19
            (eq, ":commander_party", "p_main_party"),
            (eq, ":faction_no", "$players_kingdom"),
            (assign, ":old_target_to_follow_other_party", ":commander_party"),
          (else_try),
            (gt, ":commander_party", 0),
            (assign, ":old_target_to_follow_other_party", ":commander_party"),
          (try_end), #end tr19

          (troop_get_slot, ":hero_renown", ":troop_no", slot_troop_renown),

          (assign, ":num_available_to_follow", 0),
          (try_begin), #tr20
            (eq, ":faction_no", "$players_kingdom"),
            (eq, "p_main_party", ":old_target_to_follow_other_party"),
            (val_add, ":num_available_to_follow", 1),
            (eq, "p_main_party", ":old_target_to_follow_other_party"),
            (val_add, ":num_available_to_follow", 999),
          (try_end), #end tr20
          (try_for_range, ":other_hero", kingdom_heroes_begin, kingdom_heroes_end), #tr21
            (neq, ":other_hero", ":troop_no"),
            (store_troop_faction, ":troop_faction", ":other_hero"),
            (eq, ":troop_faction", ":faction_no"),
            (troop_get_slot, ":other_party", ":other_hero", slot_troop_leaded_party),
            (gt, ":other_party", 0),
            (party_is_active, ":other_party"),
            (troop_get_slot, ":other_hero_renown", ":other_hero", slot_troop_renown),
            (lt, ":hero_renown", ":other_hero_renown"),
            (party_get_slot, ":other_commander_party", ":other_party", slot_party_commander_party),
            (assign, ":other_has_valid_commander", 0),
            (try_begin),
              (eq, ":other_commander_party", "p_main_party"),
              (eq, ":faction_no", "$players_kingdom"),
              (assign, ":other_has_valid_commander", 1),
            (else_try),
              (gt, ":other_commander_party", 0),
              (party_is_active, ":other_commander_party"),
              (assign, ":other_has_valid_commander", 1),
            (try_end),
            (eq, ":other_has_valid_commander", 0), #other party is not under command itself.
            (store_distance_to_party_from_party, ":dist", ":other_party", ":party_no"),
            (lt, ":dist", 25),
            (party_slot_eq, ":other_party", slot_party_follow_me, 1),
            (val_add, ":num_available_to_follow", 1),
            (eq, ":other_party", ":old_target_to_follow_other_party"),
            (val_add, ":num_available_to_follow", 999),
          (try_end), #end tr21 (tfr)
          (gt, ":num_available_to_follow", 0),
          (store_random_in_range, ":random_party_to_follow", 0, ":num_available_to_follow"),
          (try_begin), #tr22
            (eq, ":faction_no", "$players_kingdom"),
            (eq, "p_main_party", ":old_target_to_follow_other_party"),
            (val_sub, ":random_party_to_follow", 1),
            (try_begin), #tr23
              (eq, "p_main_party", ":old_target_to_follow_other_party"),
              (val_sub, ":random_party_to_follow", 999),
            (try_end), #end tr23
            (lt, ":random_party_to_follow", 0),
            (store_mul, ":chance", 100, "$g_average_center_value_per_faction"), #this value is calculated at the beginning of the game
            (val_div, ":chance", ":faction_center_value"),
            (val_max, ":chance", 10),
            (assign, ":chance_to_follow_other_party", ":chance"),
            (val_mul, ":chance_to_follow_other_party", 2), #trp_player is always the leader
            (assign, ":target_to_follow_other_party", "p_main_party"),
            (eq, ":old_target_to_follow_other_party", ":target_to_follow_other_party"),
            (val_mul, ":chance_to_follow_other_party", 100),
          (try_end), #end tr 22
		  
          (try_for_range, ":other_hero", kingdom_heroes_begin, kingdom_heroes_end), #tr23
            (eq, ":target_to_follow_other_party", -1),
            (neq, ":other_hero", ":troop_no"),
            (store_troop_faction, ":troop_faction", ":other_hero"),
            (eq, ":troop_faction", ":faction_no"),
            (troop_get_slot, ":other_party", ":other_hero", slot_troop_leaded_party),
            (gt, ":other_party", 0),
            (party_is_active, ":other_party"),
            (troop_get_slot, ":other_hero_renown", ":other_hero", slot_troop_renown),
            (lt, ":hero_renown", ":other_hero_renown"),
            (party_get_slot, ":other_commander_party", ":other_party", slot_party_commander_party),
            (assign, ":other_has_valid_commander", 0),
            (try_begin),
              (eq, ":other_commander_party", "p_main_party"),
              (eq, ":faction_no", "$players_kingdom"),
              (assign, ":other_has_valid_commander", 1),
            (else_try),
              (gt, ":other_commander_party", 0),
              (party_is_active, ":other_commander_party"),
              (assign, ":other_has_valid_commander", 1),
            (try_end),
            (eq, ":other_has_valid_commander", 0), #other party is not under command itself.
            (store_distance_to_party_from_party, ":dist", ":other_party", ":party_no"),
            (lt, ":dist", 25),
            (party_slot_eq, ":other_party", slot_party_follow_me, 1),
            (val_sub, ":random_party_to_follow", 1),
            (try_begin), #tr24
              (eq, ":other_party", ":old_target_to_follow_other_party"),
              (val_sub, ":random_party_to_follow", 999),
            (try_end), #end tr24
            (lt, ":random_party_to_follow", 0),
            (store_mul, ":chance", 100, "$g_average_center_value_per_faction"), #this value is calculated at the beginning of the game
            (val_div, ":chance", ":faction_center_value"),
            (val_max, ":chance", 10),
            (assign, ":chance_to_follow_other_party", ":chance"),
            (try_begin), #tr25
              (faction_slot_eq, ":faction_no", slot_faction_leader, ":other_hero"),
              (val_mul, ":chance_to_follow_other_party", 2),
            (try_end), #end tr25
            (assign, ":target_to_follow_other_party", ":other_party"),
            (eq, ":old_target_to_follow_other_party", ":target_to_follow_other_party"),
            (val_mul, ":chance_to_follow_other_party", 100),
          (try_end), #end tr23
        (try_end), #end tr16

				
		(try_begin),  # tr24 sod twan456 
		(eq, "$g_sod_deactivate_ai", 0),
		(troop_get_slot, ":initiative", ":troop_no", slot_lord_initiative),
		(val_add, ":initiative", 10),
		(val_mul, ":my_center_threat_level", 4),
		(val_add, ":initiative", ":my_center_threat_level"),
		(val_mul, ":chance_to_follow_other_party", 15),
		(val_div, ":chance_to_follow_other_party", ":initiative"),
		(try_begin),
		  (ge, ":my_center_threat_level", 6),
		  (store_sub, ":center_safety_factor", 10, ":my_center_threat_level"),
		  (val_mul, ":chance_to_follow_other_party", ":center_safety_factor"),
		  (val_div, ":chance_to_follow_other_party", 10),
		(try_end),
		(try_end),  # end tr24 sod twan456 end

        (call_script, "script_sod_faction_apply_posture_to_follow_chance", ":troop_no", ":chance_to_follow_other_party", ":target_to_follow_other_party", ":under_siege", ":my_center_threat_level"),
        (assign, ":chance_to_follow_other_party", reg0),
        (faction_get_slot, ":sod_campaign_health", ":faction_no", slot_faction_sod_campaign_health),
        (try_begin),
          (le, ":sod_campaign_health", 0),
          (call_script, "script_sod_faction_update_campaign_health", ":faction_no"),
          (assign, ":sod_campaign_health", reg0),
        (try_end),
        (try_begin),
          (ge, reg1, 55),
          (eq, ":under_siege", 0),
          (val_div, ":chance_to_follow_other_party", 4),
        (else_try),
          (ge, reg1, 35),
          (eq, ":under_siege", 0),
          (val_div, ":chance_to_follow_other_party", 2),
        (else_try),
          (le, reg1, 12),
          (ge, reg2, 75),
          (val_mul, ":chance_to_follow_other_party", 5),
          (val_div, ":chance_to_follow_other_party", 4),
        (try_end),
        (try_begin),
          (is_between, ":sod_campaign_health", 1, 35),
          (val_div, ":chance_to_follow_other_party", 3),
        (else_try),
          (is_between, ":sod_campaign_health", 35, 55),
          (val_div, ":chance_to_follow_other_party", 2),
        (else_try),
          (ge, ":sod_campaign_health", 75),
          (val_mul, ":chance_to_follow_other_party", 5),
          (val_div, ":chance_to_follow_other_party", 4),
        (try_end),
		
		(assign, ":sum_chances", ":chance_to_follow_other_party"),
		
        (val_add, ":sum_chances", 600),
        (assign, ":valid_target_to_follow", 0),
        (try_begin),
          (eq, ":target_to_follow_other_party", "p_main_party"),
          (eq, ":faction_no", "$players_kingdom"),
          (assign, ":valid_target_to_follow", 1),
        (else_try),
          (gt, ":target_to_follow_other_party", 0),
          (party_is_active, ":target_to_follow_other_party"),
          (assign, ":valid_target_to_follow", 1),
        (try_end),
        (try_begin), #tr25
          (eq, ":valid_target_to_follow", 1),
          (store_random_in_range, ":random_no", 0, ":sum_chances"),
          (try_begin),
            (val_sub, ":random_no", ":chance_to_follow_other_party"),
            (lt, ":random_no", 0),
            (party_set_slot, ":party_no", slot_party_commander_party, ":target_to_follow_other_party"),
          (else_try),
            (party_set_slot, ":party_no", slot_party_commander_party, -1),
          (try_end),
        (else_try),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
        (try_end), #end tr25
      (try_end), #end tr1
  ]),
]
