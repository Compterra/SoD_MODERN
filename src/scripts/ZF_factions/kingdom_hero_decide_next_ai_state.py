SCRIPTS = [
("kingdom_hero_decide_next_ai_state",
    [
      (store_script_param_1, ":troop_no"),
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),

        (party_get_slot, ":our_follower_strength", ":party_no", slot_party_follower_strength),
        (store_troop_faction, ":faction_no", ":troop_no"),
		(party_get_slot, ":our_strength", ":party_no", slot_party_cached_strength),
	    (faction_get_slot, ":ambition", ":faction_no", slot_faction_ambition),
		(store_sub, ":stay_strength", 33, ":ambition"),
		
		######### twan453 Should I stay or should I go
		
        (assign, ":should_i_stay", 0),
	    (assign, ":besieger_party", -1),
	
		#find current center
        (assign, ":besieger_party", -1),
        (party_get_attached_to, ":cur_center_no", ":party_no"),
        (try_begin), #tr0
          (lt, ":cur_center_no", 0),
          (party_get_cur_town, ":cur_center_no", ":party_no"),
        (try_end), #tr0
        
		(try_begin), #tr1
		  (neg|is_between, ":cur_center_no", walled_centers_begin, walled_centers_end), 
		  (assign, ":my_center_threat_level", -1),
		  (assign, ":should_i_stay", -1),
		  
		(else_try),
          (store_faction_of_party, ":cur_center_faction", ":cur_center_no"),
		  
		  (try_begin), #tr2
		  (neq, ":cur_center_faction", ":faction_no"),
     	  (assign, ":my_center_threat_level", 0),
          (else_try),
		  (call_script, "script_get_center_threat_level", ":cur_center_no"),     
		  (assign, ":my_center_threat_level", reg0),   
		  (try_end), #tr2
		(try_end), #tr1
		
		(try_begin), #tr3
             (ge, ":my_center_threat_level", 0),	
             (store_relation, ":cur_center_relation", ":cur_center_faction", ":faction_no"),			 
			     (try_begin), #tr4
				 (ge, ":cur_center_relation", 0),
				 (eq, "$g_sod_deactivate_ai", 0),
		         (lt, "$party_relative_strength", ":stay_strength"),
			     (assign, ":should_i_stay", 1),
				 (else_try),
				 (ge, ":cur_center_relation", 0),
		         (lt, "$party_relative_strength", 20),
			     (assign, ":should_i_stay", 1),
				 (else_try),
				 (lt, ":cur_center_relation", 0),
				 (assign, ":should_i_stay", -1),
				 (try_end), #tr4
		(else_try),	 
			 (gt, ":my_center_threat_level", 0),
			 (party_get_slot, ":cur_center_nearby_strength", ":cur_center_no", slot_party_nearby_friend_strength),
			 (party_get_slot, ":cur_center_own_strength", ":cur_center_no", slot_party_cached_strength),
			 
			(party_get_slot, ":besieger_party", ":cur_center_no", slot_center_is_besieged_by),
              (try_begin), #tr5
               (neg|party_is_active, ":besieger_party"),
               (assign, ":besieger_party", -1),
               (try_end),  #end tr5
			 
			 (try_begin), #tr6
			    (eq, "$g_sod_deactivate_ai", 1),
				(store_div, ":min_strength_behind", ":our_strength", 2),
				(store_sub, ":cur_center_left_strength", ":cur_center_nearby_strength", ":our_strength"),
				   (try_begin), #tr7
				   (lt, ":cur_center_left_strength", ":min_strength_behind"),
				   (assign, ":should_i_stay", 1),
				   (try_end), #tr7
			 (else_try),
             (call_script, "script_party_calculate_siege_or_not_strength", ":party_no", 1),
             (assign, ":our_strength", reg0), 			 
			 (try_begin),
			 (gt, "$g_average_lord_army_strength", 0),
			 (store_div, ":min_strength_unit", "$g_average_lord_army_strength", 20),
			 (else_try),
			 (assign, ":min_strength_unit", 0),
			 (try_end),
			 (assign, ":optimism", 35),
			 (val_sub, ":optimism", ":ambition"),
             (store_mul, ":min_strength_behind", ":min_strength_unit", ":optimism"), #155 to 205% of average
             (val_sub, ":min_strength_behind", ":optimism"),
			 (store_add, ":center_strength", ":cur_center_own_strength", ":cur_center_nearby_strength"),
			 		(try_begin), #tr8
					(ge, ":besieger_party", 0),
					(val_mul, ":min_strength_behind", 2),
					(else_try),
					(party_slot_eq, ":cur_center_no", slot_party_type, spt_town), 
					(val_mul, ":min_strength_behind", 3),
					(val_div, ":min_strength_behind", 2),
					(try_end),  #tr8
			 (try_begin),
			 (gt, ":our_strength", 0),
			 (store_div, ":minimum", ":our_strength", 10),
			 (else_try),
			 (assign, ":minimum", 0),
			 (try_end),
             (store_add, ":minimum", ":our_strength"),			 
				   (try_begin), #tr9
				       (gt, ":minimum", ":cur_center_nearby_strength"),
                       (assign, ":should_i_stay", 1),
                   (else_try),                 				   
                       (gt, ":min_strength_behind", ":center_strength"),
					   (assign, ":should_i_stay", 1),
					(try_end), #tr9
                (try_end),	#tr6	
         (try_end),  #tr3				
         
# active defense : chose to patrol instead of staying in garrison if your are stronger than nearby enemies		 
        (try_begin),  #tr10
		   (eq, "$g_sod_autoresolve", 0),
		   (eq, ":should_i_stay", 1),
		   (ge, "$party_relative_strength", 60),
		   (party_get_slot, ":enemy_str", ":cur_center_no", slot_party_nearby_enemy_strength),
		   (call_script, "script_party_calculate_siege_or_not_strength", ":party_no", 0),
           (assign, ":our_strength", reg0),
           (val_add, ":our_strength", ":our_follower_strength"),		   
		   (store_div, ":min_strength_unit", ":enemy_str", 20),
		   (assign, ":optimism", 26),
		   (val_sub, ":optimism", ":ambition"),
		   (store_mul, ":strength_needed", ":min_strength_unit", ":optimism"),
		      (try_begin), #tr11
			  (gt, ":our_strength", ":strength_needed"),
			  (gt, ":enemy_str", 100),
              (assign, ":should_i_stay", 2),
			  (try_end), #tr11
		  (try_end),	#tr10  
#twan453 end

        (party_get_slot, ":old_ai_state", ":party_no", slot_party_ai_state),
        (party_get_slot, ":old_ai_object", ":party_no", slot_party_ai_object),

        (assign, ":cancel", 0),
        (try_begin), #tr12 if we are retreating to a center keep retreating
          (eq, ":old_ai_state", spai_retreating_to_center),
          (neg|party_is_in_any_town, ":party_no"),
          (assign, ":cancel", 1),   #twan453 removed the ai state change for being in town, problems are dealt with in hotfix simple trigger
		  (else_try),
		  (troop_slot_eq, ":troop_no", slot_lord_initiative, -10),
		  (gt, ":should_i_stay", -1),
		  (assign, ":cancel", 1), # twan453 ai shouldn't be recalculated for lords keeping center just taken
        (try_end), # end tr12
		
		(try_begin), #tr13
        (eq, ":cancel", 0),

        ##        (faction_get_slot, ":faction_ai_state",  ":faction_no", slot_faction_ai_state),
        ##        (faction_get_slot, ":faction_ai_object", ":faction_no", slot_faction_ai_object),

        (faction_get_slot, ":num_towns", ":faction_no", slot_faction_num_towns),
        (store_mul, ":faction_center_value", ":num_towns", 2),
        (faction_get_slot, ":num_castles", ":faction_no", slot_faction_num_castles),
        (val_add, ":faction_center_value", ":num_castles"),
        (val_mul, ":faction_center_value", 10),
        (val_max, ":faction_center_value", 5),

        (assign, ":chance_move_to_home_center", 0),
        (assign, ":target_move_to_home_center", -1),
        (assign, ":chance_move_to_other_center", 0),
        (assign, ":target_move_to_other_center", -1),
        (assign, ":chance_besiege_enemy_center", 0),
        (assign, ":target_besiege_enemy_center", -1),
        (assign, ":chance_patrol_around_center", 0),
        (assign, ":target_patrol_around_center", -1),
        (assign, ":chance_raid_around_center", 0),
        (assign, ":target_raid_around_center", -1),
        (assign, ":chance_recruit_troops", 0),
        (assign, ":target_recruit_troops", -1),
		
		(assign, ":home_center_threat_level", -1),
		(assign, ":other_center_threat_level", -1),
		(assign, ":patrol_threat_level", -1),
		
#Moving to home center ##################################
        (try_begin), #tr14
          (le, ":should_i_stay", 0),
          (assign, ":old_target_move_to_home_center", -1),
				  (try_begin), #tr15
					(eq, ":old_ai_state", spai_holding_center),
					(assign, ":old_target_move_to_home_center", ":old_ai_object"), 
				  (try_end), #end tr15
				  (try_begin), #tr16
					(is_between, ":cur_center_no", centers_begin, centers_end), #already in our center
					(party_slot_eq,  ":cur_center_no", slot_town_lord, ":troop_no"),
					(assign, ":target_move_to_home_center", ":cur_center_no"),
					(assign, ":chance_move_to_home_center", 100), 					  
				  (try_end), #end tr16
				  (try_begin), #tr17
					(eq, ":target_move_to_home_center", -1), #twan453                 
					(call_script, "script_cf_troop_get_random_leaded_walled_center_with_less_strength_priority", ":troop_no", ":old_target_move_to_home_center"), #Can fail
					(assign, ":target_move_to_home_center", reg0),
					(assign, ":chance_move_to_home_center", 50),
						(try_begin), #tr18
						  (eq, ":old_target_move_to_home_center", ":target_move_to_home_center"),
						  (val_mul, ":chance_move_to_home_center", 100),
						(try_end), #end tr18
				(try_end), #end tr17
			  (try_begin), #tr19
			     (eq, ":target_move_to_home_center", -1),
				 (eq, ":cur_center_no", -1), 
				 (assign, ":chance_move_to_home_center", 0),
			  (else_try),
			      (eq, ":target_move_to_home_center", -1),
			  	  (party_slot_eq,  ":cur_center_no", slot_town_lord, ":troop_no"),
                  (assign, ":target_move_to_home_center", ":cur_center_no"),		  
              (try_end),	#end tr19			
				
			    (try_begin), # tr20 twan new
				 (is_between, ":target_move_to_home_center", centers_begin, centers_end),
                 (call_script, "script_get_center_threat_level", ":target_move_to_home_center"),
				 (assign, ":home_center_threat_level", reg0),
                 (try_begin),#tr21
				    (neq, ":cur_center_faction", ":faction_no"),
					(val_mul, ":chance_move_to_home_center", 10), #twanx leave other factions centers asap
					(else_try),
                    (lt, ":home_center_threat_level", ":my_center_threat_level"),  # stay in more threatened centers with some chances to go home
					(neq, ":target_move_to_home_center", ":cur_center_no"),
					(neq, ":target_move_to_home_center", ":old_target_move_to_home_center"),
                    (val_div, ":chance_move_to_home_center", ":my_center_threat_level"),
					(val_max, ":chance_move_to_home_center", 1),
					(else_try),
                    (eq, ":home_center_threat_level", 0),
					(eq, ":cur_center_no", ":target_move_to_home_center"),  # leave home center more often if not threatened
                    (val_div, ":chance_move_to_home_center", 7),		
                    (val_mul, ":chance_move_to_home_center", 6),
                    (val_max, ":chance_move_to_home_center", 1), 					
                 (try_end), #end tr21		   
               (try_end), #end tr20 twan new					
		 (try_end), #end tr14	
        
	     
	   
	   #Moving to other center
          (try_begin), #tr22
			(ge, ":should_i_stay", 1),
            (assign, ":chance_move_to_other_center", 50000),
            (assign, ":target_move_to_other_center", ":cur_center_no"),
			   (try_begin), #tr23
			   (party_slot_eq, ":cur_center_no", slot_town_lord, ":troop_no"), #if other center = home center use home center chance instead
			   (assign, ":chance_move_to_home_center", 50000),                 #twan453 for coherence of bonuses 
			   (assign, ":target_move_to_home_center", ":cur_center_no"),
			   (assign, ":chance_move_to_other_center", 0),
               (assign, ":target_move_to_other_center", -1),
			   (try_end), #tr23
          (else_try),
            (assign, ":old_target_move_to_other_center", -1),
				(try_begin), #tr24
				  (eq, ":old_ai_state", spai_holding_center),
				  (assign, ":old_target_move_to_other_center", ":old_ai_object"),
				(try_end),  #end tr24
				
            (try_begin), #tr25
              (eq, ":target_move_to_other_center", -1),
			  (store_random_in_range, ":rnd", 0, 100),
				(try_begin), #tr26
					(eq, ":should_i_stay", 0),
					(this_or_next|lt, ":rnd", 50), # 50% chance to stay when lord isn't forced to 
                    (eq, "$g_sod_deactivate_ai", 1),					
					(is_between, ":cur_center_no", centers_begin, centers_end),
					(ge, ":cur_center_relation", 0),
					(assign, ":chance_move_to_other_center", 500),
					(assign, ":target_move_to_other_center", ":cur_center_no"),
				  (else_try),
					(call_script, "script_cf_select_random_walled_center_with_faction_and_less_strength_priority", ":faction_no", ":old_target_move_to_other_center"),
					(assign, ":target_move_to_other_center", reg0),
					(assign, ":chance_move_to_other_center", 10),
					(party_get_slot, ":lord_of_center", ":target_move_to_other_center", slot_town_lord),
						(try_begin), #tr27
						  (call_script, "script_cf_troop_check_troop_is_enemy", ":troop_no", ":lord_of_center"),
						  (assign, ":chance_move_to_other_center", 1),
						(try_end), #tr27
						
					(try_begin), # tr28 twan new
		            (eq, "$g_sod_deactivate_ai", 0),
		            (call_script, "script_get_most_threatened_close_walled_center", ":party_no"),
					   (try_begin),#tr29
					   (is_between, reg1, centers_begin, centers_end),
					   (assign, ":target_move_to_other_center", reg1),
					   (assign, ":chance_move_to_other_center", reg2),
                       (try_end),		# end tr29 	
                    (try_end), 	#end tr28		twan new	
					
					(try_begin),  #tr29
					  (eq, ":old_target_move_to_other_center", ":target_move_to_other_center"),
					  (val_mul, ":chance_move_to_other_center", 100),
					(try_end), #end tr29
			    (try_end), #end tr26						
				(try_end), #end tr25
      
        (try_begin), #tr30
          (lt, "$party_relative_strength", 50),
		  (eq, "$g_sod_deactivate_ai", 1),
          (store_sub, ":factor", 100, "$party_relative_strength"),
			  (try_begin), #tr31
				(gt, ":chance_move_to_home_center", 0),				
				(val_mul, ":chance_move_to_home_center", 200),
				(val_div, ":chance_move_to_home_center", ":factor"),
			   (else_try),
				(val_mul, ":chance_move_to_other_center", 200),
				(val_div, ":chance_move_to_other_center", ":factor"),
			  (try_end), #end tr31
		   (else_try),
		   (is_between, "$party_relative_strength", 1, 70),           #twan454
           (gt, ":chance_move_to_home_center", 0),
		   (this_or_next|eq, ":should_i_stay", -1),
		   (eq, ":target_move_to_home_center", ":cur_center_no"),
		   (val_mul, ":chance_move_to_home_center", 100),
           (val_div, ":chance_move_to_home_center", "$party_relative_strength"),
		   (else_try),
		   (is_between, "$party_relative_strength", 1, 70),
           (gt, ":chance_move_to_other_center", 0),
		   (this_or_next|eq, ":should_i_stay", -1),
		   (eq, ":target_move_to_other_center", ":cur_center_no"),
  		   (val_mul, ":chance_move_to_other_center", 80),
           (val_div, ":chance_move_to_other_center", "$party_relative_strength"),
           (else_try),
		   (gt, "$party_relative_strength", 80),
		   (val_mul, ":chance_move_to_other_center", 70),
		   (val_div, ":chance_move_to_other_center", "$party_relative_strength"),		   #twan454
        (try_end), #end tr30

        (try_begin), #tr32
          (gt,  "$ratio_of_prisoners", 50),
          (try_begin), #tr33
            (gt, ":chance_move_to_home_center", 0),
            (val_mul, ":chance_move_to_home_center", 2),
          (else_try),
            (val_mul, ":chance_move_to_other_center", 2),
          (try_end), #end tr33
        (try_end), #end tr32
		
           (try_begin),  # tr34 
           (is_between, ":target_move_to_other_center", walled_centers_begin, walled_centers_end),		   
		   (call_script, "script_get_center_threat_level", ":target_move_to_other_center"),
		   (assign, ":other_center_threat_level", reg0),
                 (try_begin), #tr35
				 	(neq, ":cur_center_faction", ":faction_no"),
					(val_mul, ":chance_move_to_home_center", 10),  #twanx leave other factions centers to owned center asap
				 (else_try),
					(this_or_next|lt, ":other_center_threat_level", ":home_center_threat_level"),
                    (lt, ":other_center_threat_level", ":my_center_threat_level"),  # avoid moves to less threatened other centers
					(neq, ":target_move_to_other_center", ":old_target_move_to_other_center"), # except if you are already moving
                    (val_div, ":chance_move_to_other_center", 10),
				 (else_try),
				    (gt, ":chance_move_to_other_center", 1),
                    (le, ":other_center_threat_level", 0),
					(ge, "$party_relative_strength", 80),
					(le,  "$ratio_of_prisoners", 50),
                    (val_div, ":chance_move_to_other_center", 3),	# no need to go to other non threatened centers	except if the party is weakened	or has a lot of prisoners		
                    (val_max, ":chance_move_to_other_center", 1),
				 (try_end), #end tr35 				
		  (else_try),
          (assign, ":target_move_to_other_center", -1),
          (assign, ":chance_move_to_other_center", 0), 	
	     (try_end),	# end tr34
		 
	(try_end), # end tr22
		
		
#Recruiting troops ################################
        (try_begin), #tr36
          (le, ":should_i_stay", 0),
		  (lt, "$party_relative_strength", 70),
		  (le,  "$ratio_of_prisoners", 90),
          (assign, ":old_target_recruit_troops", -1),
          (try_begin), #tr37
            (eq, ":old_ai_state", spai_recruiting_troops),
            (assign, ":old_target_recruit_troops", ":old_ai_object"),
          (try_end), #end tr37
          (troop_get_slot, ":original_faction", ":troop_no", slot_troop_original_faction),
          (faction_get_slot, ":original_faction_culture", ":original_faction", slot_faction_culture),
          (assign, ":compare", 1),  #twan453 begin
          
		  (try_for_range, ":village_no", villages_begin, villages_end),  #tr38
            (store_faction_of_party, ":village_faction_no", ":village_no"),
            (store_relation, ":reln", ":village_faction_no", ":faction_no"),
            (ge, ":reln", 0),
			(assign, ":score", 0),
			(store_distance_to_party_from_party, ":real_dist", ":village_no", ":party_no"),
			
			(try_begin), #tr39
			  (le, ":real_dist", 50), # exclude all villages more than 50 dist away
			
				  (try_begin), #tr40
				  (party_slot_eq, ":village_no", slot_center_culture, ":original_faction_culture"),
				  (val_add, ":score", 1),
					(try_begin), #tr41
					  (eq, ":village_faction_no", ":faction_no"),
					  (val_add, ":score", 20),
					(try_end), #end tr41
				  (try_end), #tr40

				  (try_begin), #tr42
				  (eq, "$g_sod_deactivate_ai", 0),
				  (call_script, "script_calculate_dist_factor", ":troop_no", ":village_no"),
				  (store_sub, ":dist_factor", 100, reg0),
				  (val_max, ":dist_factor", 10),	
				  (val_mul, ":score", ":dist_factor"),
				  (else_try),
				  (store_sub, ":dist_factor", 100, ":real_dist"),
				  (val_mul, ":score", ":dist_factor"),
				  (try_end), #tr42
				  
				  (party_get_slot, ":volunteer_amount", ":village_no", slot_center_npc_volunteer_troop_amount),
				  (val_mul, ":score", ":volunteer_amount"),

				(assign, ":raid_factor", 100),
					(try_begin),  #tr43
					  (party_slot_eq, ":village_no", slot_village_state, svs_being_raided),
					  (assign, ":raid_factor", 1),
					(try_end),   #endtr43

				(val_mul, ":score", ":raid_factor"),
							
				(try_begin),  #tr44
				  (eq, ":village_no", ":old_target_recruit_troops"),
				  (val_mul, ":score", 100),
				(try_end),   #end tr44
				
				(try_for_range, ":khero", kingdom_heroes_begin, kingdom_heroes_end), #tr45 other lords factor
				(neq, ":khero", ":troop_no"),
				(troop_get_slot, ":hero_party", ":khero", slot_troop_leaded_party),
				(gt, ":hero_party", 0),
				(party_is_active, ":hero_party"),
					 (try_begin),  #tr46
					 (party_slot_eq, ":hero_party", slot_party_ai_state, spai_recruiting_troops),
					 (party_slot_eq, ":hero_party", slot_party_ai_object, ":village_no"),
					 (assign, ":score", 0),  #twan454 make so several lords don't go to the same village
					 (try_end), #tr46
				(try_end), #tr45

              (try_end), #tr39
                   
				 (try_begin), #tr47
                 (gt, ":score", ":compare"),
                 (assign, ":compare", ":score"),
                 (assign, ":target_recruit_troops", ":village_no"),
				 (assign, ":chance_recruit_troops", 3),
                 (try_end), #tr47
           (try_end), #tr39 end tfr villages 				 
				
		
			  (try_begin), #tr48
				  (eq, ":old_target_recruit_troops", ":target_recruit_troops"),
				  (val_mul, ":chance_recruit_troops", 1000),
				  (else_try),
				  (eq, "$g_sod_deactivate_ai", 0),
				  (le, ":my_center_threat_level", 0),
				  (le, ":home_center_threat_level", 0),
				  (le, ":other_center_threat_level", 0),
				  (val_mul, ":chance_recruit_troops", 3),
				(try_end), #end tr 48
		(try_end), #tr36
		
		
		
 #raid villages  #################################		
        (try_begin),  #tr49
          (eq, ":besieger_party", -1),
		  (le, ":should_i_stay", 0),
          (gt, "$party_relative_strength", 60),
          (lt,  "$ratio_of_prisoners", 50),
          (assign, ":old_target_raid_around_center", -1),
          (try_begin), #tr50
            (eq, ":old_ai_state", spai_raiding_around_center),
            (assign, ":old_target_raid_around_center", ":old_ai_object"),
          (try_end), #end tr50
          (assign, ":compare", 1),
		  
          (try_for_range, ":enemy_village_no", villages_begin, villages_end), #tr47
            (call_script, "script_get_center_faction_relation_including_player", ":enemy_village_no", ":faction_no"),
            (lt, reg0, 0),
			(assign, ":center_relation", reg0),
			(assign, ":score", 0),
            (assign, ":raided_by_self", 0),
		    (store_distance_to_party_from_party, ":real_dist", ":enemy_village_no", ":party_no"),
	
            (try_begin), #tr48
              (party_slot_eq, ":enemy_village_no", slot_village_state, svs_being_raided),
              (party_slot_eq, ":enemy_village_no", slot_village_raided_by, ":party_no"),
              (assign, ":raided_by_self", 1),
            (try_end), #end tr48
    
	        (try_begin), #tr49  
        	(this_or_next|party_slot_eq, ":enemy_village_no", slot_village_state, 0), #village is not already raided
            (eq, ":raided_by_self", 1),
			(lt, ":real_dist", 80),

					(try_begin), #tr50
					(eq, "$g_sod_deactivate_ai", 0),
					(str_store_string, s33, "@Call 3"),
					(call_script, "script_calculate_dist_factor", ":troop_no", ":enemy_village_no"),  # SoD Twan adjusted dist
					(assign, ":dist", reg0), 
					(store_sub, ":dist_factor", 75, ":dist"),  
					(val_max, ":dist_factor", 3),
					(call_script, "script_get_center_relative_value",":enemy_village_no"),  # Sod Twan increase chances to raid rich villages
					(val_max, reg0, 25),
					(store_mul, ":score", reg0, ":dist_factor"),
					(else_try),
					(store_sub, ":dist_factor", 75, ":real_dist"),
				    (store_random_in_range, ":rnd", 1, 20),
					(store_mul, ":score", ":rnd", ":dist_factor"),
					(try_end), #tr50					
					
					(store_random_in_range, ":rnd", 10, 15), # a little random factor
					(val_mul, ":score", ":rnd"),
					
					(val_mul, ":center_relation", -1),
					(val_max, ":center_relation", 50),
					(val_mul, ":score", ":center_relation"),
					
					 (try_begin), #tr51
						(eq, ":enemy_village_no", ":old_target_raid_around_center"),
						(val_mul, ":score", 1000),
					  (try_end), #tr51
             (try_end), #tr49
			
			(try_begin), #tr52
			   (gt, ":score", ":compare"),
			   (assign, ":compare", ":score"),
			   (assign, ":target_raid_around_center", ":enemy_village_no"),
			   (assign, ":chance_raid_around_center", 5),
            (try_end), 	#tr52

           (try_end), #end tr47 (try for range)			
		  
            (try_begin), #tr53
              (eq, ":old_target_raid_around_center", ":target_raid_around_center"),
              (val_mul, ":chance_raid_around_center", 100),
			  (else_try),
              (eq, "$g_sod_deactivate_ai", 0), # twan new
			  (eq, ":my_center_threat_level", 0),  # let's make something offensive when there is nothing defensive to do
			  (eq, ":home_center_threat_level", 0),
			  (eq, ":other_center_threat_level", 0), 
              (val_mul, ":chance_raid_around_center", 3), # twan new 			  
            (try_end), #end tr53
		  
        (try_end), #end tr49
	 

		 #besiege center#####################################		 
        (try_begin), #tr54
          (le, ":should_i_stay", 0),
		  (le,  "$ratio_of_prisoners", 60),

          (assign, ":continue", 0),
			  (try_begin), #tr55
				(eq, ":old_ai_state", spai_besieging_center),
				(gt, "$party_relative_strength", 50),
				(assign, ":continue", 1),
			  (else_try), 
				(gt, "$party_relative_strength", 80),
				(lt, "$ratio_of_prisoners", 50),
				(assign, ":continue", 1),
			  (try_end), #end tr55
			  
		  (try_begin), #tr56	  
          (eq, ":continue", 1),

		  (try_begin), #tr57
		  (eq, "$g_sod_deactivate_ai", 0),
		  (call_script, "script_party_calculate_siege_or_not_strength", ":party_no", 1),
		  (assign, ":our_strength", reg0),
		  (troop_get_slot, ":self_confidence", ":troop_no", slot_lord_self_confidence), # Twan
		  (val_mul, ":our_strength", ":self_confidence"),
		  (val_div, ":our_strength", 100),
		  (else_try),
		  (party_get_slot, ":our_strength", ":party_no", slot_party_cached_strength),
		  (try_end), #tr57
		  
          (assign, ":our_estimated_str", ":our_follower_strength"),
          (val_add, ":our_estimated_str", ":our_strength"),

          (assign, ":old_target_besiege_enemy_center", -1),
          
		  (try_begin), #tr58
            (eq, ":old_ai_state", spai_besieging_center),
            (assign, ":old_target_besiege_enemy_center", ":old_ai_object"),
          (try_end), #end tr58

          (assign, ":best_besiege_center", -1),
          (assign, ":best_besiege_center_score", 0),
		  
          (try_for_range, ":enemy_walled_center", walled_centers_begin, walled_centers_end), #tr59
            (party_get_slot, ":other_besieger_party", ":enemy_walled_center", slot_center_is_besieged_by),
            (assign, ":besieger_own_faction", 0),
			(assign, ":center_score", -1),
			
			(try_begin), #tr60
              (ge, ":other_besieger_party", 0),
              (party_is_active, ":other_besieger_party"),
              (store_faction_of_party, ":besieger_faction", ":other_besieger_party"),
              (eq, ":besieger_faction", ":faction_no"),
              (assign, ":besieger_own_faction", 1),
            (try_end), #end tr60
			
			(try_begin), #tr61
            (this_or_next|eq, ":other_besieger_party", -1),
            (eq, ":besieger_own_faction", 1),
            (call_script, "script_get_center_faction_relation_including_player", ":enemy_walled_center", ":faction_no"),
            (assign, ":reln", reg0),
            (lt, ":reln", 0),
            (val_mul, ":reln", -1),
            (val_add, ":reln", 50),
            (call_script, "script_calculate_dist_factor", ":troop_no", ":enemy_walled_center"),  # SoD Twan adjusted dist
            (assign, ":dist", reg0), 
            (store_sub, ":dist_factor", 75, ":dist"),                                           # SoD Twan ends  
            (val_max, ":dist_factor", 3),
            (party_get_slot, ":center_str", ":enemy_walled_center", slot_party_cached_strength),
            (party_get_slot, ":center_near_str", ":enemy_walled_center", slot_party_nearby_friend_strength),
            (val_add, ":center_str", ":center_near_str"),

            (store_mul, ":relative_center_str", ":center_str", 100),
            (val_div, ":relative_center_str", ":our_estimated_str"),
            (store_sub, ":center_score", 1000, ":relative_center_str"),
            (val_max, ":center_score", 1),

            (val_mul, ":center_score", ":reln"),
            (val_mul, ":center_score", ":dist_factor"),
			
				(try_begin), #tr62
				  (party_slot_eq, ":enemy_walled_center", slot_town_lord, "trp_player"),
				  (call_script, "script_troop_get_player_relation", ":troop_no"),
				  (assign, ":player_relation", reg0),
				  (lt, ":player_relation", 0),
				  (store_sub, ":multiplier", 50, ":player_relation"),
				  (faction_get_slot, ":badboy", "fac_player_supporters_faction", slot_faction_badboy_rating), #twan454
				  (val_add, ":multiplier", ":badboy"),
				  (val_mul, ":center_score", ":multiplier"),
				  (val_div, ":center_score", 50),
				(try_end), #end tr62
				
				(try_begin), #tr63
				  (eq, ":enemy_walled_center", ":old_target_besiege_enemy_center"),
				  (val_mul, ":center_score", 200),
				(try_end), #end tr63
				
			(call_script, "script_adjust_ai_value_with_center_value", ":center_score", ":enemy_walled_center"),  # SoD Twan give priority to rich centers
            (assign, ":center_score", reg0),
			
		(try_end), #tr61
				(try_begin), #tr64
				  (gt, ":center_score", ":best_besiege_center_score"),
				  (assign, ":best_besiege_center_score", ":center_score"),
				  (assign, ":best_besiege_center", ":enemy_walled_center"),
				(try_end), #end tr64
          (try_end), #end tr59 (try for range)
          
		  (try_begin), #tr65
          (ge, ":best_besiege_center", 0),
          (assign, ":chance_besiege_enemy_center", 20),
          (assign, ":target_besiege_enemy_center", ":best_besiege_center"),
			  (try_begin), #tr66
				(eq, ":old_target_besiege_enemy_center", ":target_besiege_enemy_center"),
				(val_mul, ":chance_besiege_enemy_center", 500),
			  (try_end),  #end tr66
          (try_end), #tr 65
				
		  (try_begin), #tr64
		  (eq, "$g_sod_deactivate_ai", 0), # twan new
		  (eq, ":my_center_threat_level", 0),  # let's make something offensive when there is nothing defensive to do
		  (eq, ":home_center_threat_level", 0),
		  (eq, ":other_center_threat_level", 0), 
		  (ge, ":ambition", 0),
		  (val_mul, ":chance_besiege_enemy_center", 3), # twan new 
		  (try_end), #end tr64
		  
		  (try_begin), #tr64b
		  (eq, "$g_sod_deactivate_lords_ai", 0),
		  (faction_slot_eq, ":faction_no", slot_faction_offensive_objective, ":target_besiege_enemy_center"),
		  (neg|troop_slot_ge, ":troop_no", slot_lord_initiative, 4),
		  (val_mul, ":chance_besiege_enemy_center", 3),
		  (else_try),
		  (eq, "$g_sod_deactivate_lords_ai", 0),
		  (troop_slot_ge, ":troop_no", slot_lord_initiative, 4),
		  (troop_slot_eq, ":troop_no", slot_lord_personnal_objective, ":target_besiege_enemy_center"),
		  (val_mul, ":chance_besiege_enemy_center", 3),
		  (try_end), #tr64b
		  
		 (try_end), #end tr56
		 (try_end), #tr54
	

#patrol alarmed center. #####################################		
        (try_begin), #tr65
		  (eq, ":should_i_stay", 2),
		  (assign, ":target_patrol_around_center", ":cur_center_no"),
		  (assign, ":chance_patrol_around_center", 50000),  #twan453 active defense
		  (else_try),
          (le, ":should_i_stay", 0),
          (ge, "$party_relative_strength", 60),
		  (le,  "$ratio_of_prisoners", 60),
		  
          (try_begin), # tr66
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_patrolling_around_center),
            (party_get_slot, ":target_patrol_around_center", ":party_no", slot_party_ai_object),
          (try_end), #end tr66

          (assign, ":old_target_patrol_around_center", -1),
          (try_begin), #tr67
            (eq, ":old_ai_state", spai_patrolling_around_center),
            (assign, ":old_target_patrol_around_center", ":old_ai_object"),
          (try_end), #end tr67

          (assign, ":best_patrol_score", 0),
          (assign, ":best_patrol_target", -1),
		  
          (try_for_range, ":center_no", centers_begin, centers_end), #tr68 #find closest center that has spotted enemies.
            (store_faction_of_party, ":center_faction", ":center_no"),
            (eq, ":center_faction", ":faction_no"),
		   (str_store_string, s33, "@Call 6"),
           (call_script, "script_calculate_dist_factor", ":troop_no", ":center_no"), # Sod Twan adjusted dist
           (assign, ":distance", reg0),  
		   (store_sub, ":this_center_score", 100, ":distance"),
            (val_max, ":this_center_score", 1),
            (try_begin), #tr69
              (party_slot_ge, ":center_no", slot_center_last_spotted_enemy, 0),
              (val_mul, ":this_center_score", 100),
            (try_end), #end tr69
            (try_begin), #tr70
              (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
              (val_mul, ":this_center_score", 2),
            (try_end), #end tr70
            (try_begin), #tr71
              (eq, ":center_no", ":old_target_patrol_around_center"),
              (val_mul, ":this_center_score", 1000),
            (try_end), #end tr71
			(call_script, "script_adjust_ai_value_with_center_value", ":this_center_score", ":center_no"),  # SoD Twan center value
			(assign, ":this_center_score", reg0),
            (try_begin), #tr72
              (gt, ":this_center_score", ":best_patrol_score"),
              (assign, ":best_patrol_score", ":this_center_score"),
              (assign, ":best_patrol_target", ":center_no"),
            (try_end), #end tr72
          (try_end), #end tr68 (try fir range)
		  
          (try_begin), #tr73
            (gt, ":best_patrol_score", 0),
            (assign, ":target_patrol_around_center", ":best_patrol_target"),
          (try_end), #end tr73
		  
          (try_begin), #tr74
            (is_between, ":target_patrol_around_center", centers_begin, centers_end),
            (assign, ":chance_patrol_around_center", 15),
          (try_end), #end tr74
          
		  (try_begin), #tr75
            (troop_slot_ge, ":troop_no", slot_troop_change_to_faction, 1),
            (val_mul, ":chance_patrol_around_center", 3),
          (try_end), #end tr75
          
		  (try_begin), #tr76
            (eq, ":old_target_patrol_around_center", ":target_patrol_around_center"),
            (val_mul, ":chance_patrol_around_center", 20),
          (try_end), #end tr 76	

		(try_begin), # tr77 twan new
		(eq, "$g_sod_deactivate_ai", 0),
		(is_between, ":target_patrol_around_center", centers_begin, centers_end),
        (call_script, "script_get_center_threat_level", ":target_patrol_around_center"),
		(assign, ":patrol_threat_level", reg0),
		     (try_begin), # tr78
                    (lt, ":patrol_threat_level", ":my_center_threat_level"),  # reduce the chance to leave a center to patroll another less threatened center
					(neq, ":target_patrol_around_center", ":cur_center_no"),     # allow to patrol around a threatened center you are in
                    (val_div, ":chance_patrol_around_center", 2),
			  (else_try),
                    (eq, ":other_center_threat_level", 0),
					(eq, ":home_center_threat_level", 0),
					(eq, ":my_center_threat_level", 0),
                    (val_mul, ":chance_patrol_around_center", ":patrol_threat_level"),	# give priority to patrols if threat level is high and there is no other threats		
              (try_end), #end tr78	 
      (try_end),  # tr77 twan new
				 				 
	(try_end), #end tr65
	

	
########## FINAL CHANCES ADJUSTMENTS	

	  # (try_begin),
      # (eq, "$g_sod_debug", 1),	  
	  # (str_store_troop_name, s12, ":troop_no"),   #debug (make log text very long uncomment for tests)
	  # (assign, reg4, ":chance_move_to_home_center"),
	  # (assign, reg5, ":chance_move_to_other_center"),
	  # (assign, reg6, ":chance_besiege_enemy_center"),
	  # (assign, reg7, ":chance_patrol_around_center"),
	  # (display_log_message, "@{s12} chances before adjustments  home {reg4} other {reg5} besiege {reg6} patrol {reg7}", debug_color),  # debug end
	  # (try_end),	

        (troop_get_slot, ":self_confidence", ":troop_no", slot_lord_self_confidence),
	    (troop_get_slot, ":initiative", ":troop_no", slot_lord_initiative),
	    (troop_get_slot, ":raiding_factor", ":troop_no", slot_lord_raiding_factor), 
		(troop_get_slot, ":interception_factor", ":troop_no", slot_lord_interception_factor),
		(store_sub, ":garrisoning_factor", 200, ":interception_factor"),
		(val_max, ":garrisoning_factor", 0),
	    (store_add, ":sieging_factor", ":garrisoning_factor", ":self_confidence"),   
	    (val_div, ":sieging_factor", 2),                                             
       
		
		(try_begin), #tr79
		  (gt, ":chance_move_to_home_center", 1),		
		(try_begin), #tr80 
			  (eq, "$g_sod_deactivate_ai", 0),     
			  (gt, ":target_move_to_home_center", 0),
			  (str_store_string, s33, "@Call 7"),
			  (call_script, "script_calculate_dist_factor", ":troop_no", ":target_move_to_home_center"),	
       			  (try_begin), #tr81 
				  (lt, reg0, 30),
				  (assign, ":bonus", 20),
				  (else_try),
				  (gt, reg0, 50),
				  (assign, ":bonus", -20),
				  (try_end), #end tr81
			  (val_max, ":initiative", 1),
			  (val_mul, ":chance_move_to_home_center", 2),
			  (val_div, ":chance_move_to_home_center", ":initiative"),
	    (else_try),
             (assign, ":bonus", 0),			  
	    (try_end),   #end tr82
			  (val_add, ":bonus", ":garrisoning_factor"),
			  (val_mul, ":chance_move_to_home_center", ":bonus"),                                                          
			  (val_div, ":chance_move_to_home_center", 100),    
			  (call_script, "script_adjust_ai_value_with_center_value", ":chance_move_to_home_center", ":target_move_to_home_center"),  # Sod Twan make ai garrison rich centers more often
			  (assign, ":chance_move_to_home_center", reg0),
		(try_end),	 # end tr82 
		
        (try_begin), #tr83
         (gt, ":chance_move_to_other_center", 1), 		
		 (try_begin), #tr84
			  (eq, "$g_sod_deactivate_ai", 0),                              # SoD Twan added a dist factor to increase chances of garrisoning strategic/close places
			  (gt, ":target_move_to_other_center", 0),
			  (str_store_string, s33, "@Call 8"),
			  (call_script, "script_calculate_dist_factor", ":troop_no", ":target_move_to_other_center"),	
       			  (try_begin), #tr85 
				  (lt, reg0, 30),
				  (assign, ":bonus", 20),
				  (else_try),
				  (gt, reg0, 50),
				  (assign, ":bonus", -20),
				  (try_end), #end tr85
			  (val_max, ":initiative", 1),
			  (val_mul, ":chance_move_to_other_center", 2),
			  (val_div, ":chance_move_to_other_center", ":initiative"),
		(else_try),
              (assign, ":bonus", 0),			  
	    (try_end),  #end tr84
		(try_end), #end tr83 
		
	 (try_begin), #tr86	
		  (val_add, ":bonus", ":garrisoning_factor"),	 
   		  (val_mul, ":chance_move_to_other_center", ":bonus"),                                                          
		  (val_div, ":chance_move_to_other_center", 100),    		
		  (call_script, "script_adjust_ai_value_with_center_value", ":chance_move_to_other_center", ":target_move_to_other_center"), 
		  (assign, ":chance_move_to_other_center", reg0),
	 (try_end), #end tr86
                              
     (try_begin), #tr87
         (gt, ":chance_raid_around_center", 1),
         (eq, "$g_sod_deactivate_ai", 0),		 
		 (val_mul, ":chance_raid_around_center", 2),
			(try_begin), #tr88
			  (eq, "$g_sod_deactivate_ai", 0),     
			  (str_store_string, s33, "@Call 9"),
			  (call_script, "script_calculate_dist_factor", ":troop_no", ":target_raid_around_center"),	
       			  (try_begin), #tr89 
				  (lt, reg0, 20),
				  (assign, ":bonus", 20),
				  (else_try),
				  (gt, reg0, 40),
				  (assign, ":bonus", -20),
				  (try_end), #end tr89
	           (val_add, ":raiding_factor", ":bonus"),
         (try_end), #tr88  			 
		 (val_mul, ":chance_raid_around_center", ":raiding_factor"),
		 (val_div, ":chance_raid_around_center", 100),
		 (call_script, "script_adjust_ai_value_with_center_value", ":chance_raid_around_center", ":target_raid_around_center"),  
         (assign, ":chance_raid_around_center", reg0),			   
     (try_end), #end tr87    
	
	(try_begin), #tr90
	    (gt, ":chance_besiege_enemy_center", 1),
		(eq, "$g_sod_deactivate_ai", 0),
		(val_mul, ":chance_besiege_enemy_center", 2),
    	(val_mul, ":chance_besiege_enemy_center", ":sieging_factor"),
		(val_div, ":chance_besiege_enemy_center", 100),
		(store_sub, ":multiplier", ":initiative", 3),
		(val_max, ":multiplier", 1),
		(val_mul, ":chance_besiege_enemy_center", ":multiplier"),
		(call_script, "script_adjust_ai_value_with_center_value", ":chance_besiege_enemy_center", ":target_besiege_enemy_center"),
		(assign, ":chance_besiege_enemy_center", reg0),                          
	 (try_end), # end tr90

   	 (try_begin), # tr91
	    (gt, ":chance_patrol_around_center", 1),
		(eq, "$g_sod_deactivate_ai", 0),
	    (val_mul, ":chance_patrol_around_center", 2),
		(val_mul, ":chance_patrol_around_center", ":interception_factor"),  
		(val_div, ":chance_patrol_around_center", 100),
		(call_script, "script_adjust_ai_value_with_center_value", ":chance_patrol_around_center", ":target_patrol_around_center"),
		(assign, ":chance_patrol_around_center", reg0),     
	  (try_end), #end tr91
		
		(assign, ":sum_chances", ":chance_move_to_home_center"),
        (val_add, ":sum_chances", ":chance_move_to_other_center"),
        (val_add, ":sum_chances", ":chance_recruit_troops"),
        (val_add, ":sum_chances", ":chance_raid_around_center"),
        (val_add, ":sum_chances", ":chance_besiege_enemy_center"),
        (val_add, ":sum_chances", ":chance_patrol_around_center"),

		
	   (try_begin), #tr92
       (eq, "$g_sod_debug", 1),	  
	   (str_store_troop_name, s12, ":troop_no"),   #debug take nords as example
	   (eq, ":faction_no", "fac_kingdom_4"),
	   (assign, reg3, ":sum_chances"),
	   (assign, reg4, ":chance_move_to_home_center"),
	   (assign, reg5, ":chance_move_to_other_center"),
	   (assign, reg6, ":chance_besiege_enemy_center"),
	   (assign, reg7, ":chance_patrol_around_center"),
	   (assign, reg8, ":chance_recruit_troops"),
	   (display_log_message, "@{s12} final chances total {reg3} home {reg4} other {reg5} besiege {reg6} patrol {reg7} recruit {reg8}", debug_color),  
	   (try_end), #end tr92	
		
		
        (val_max, ":sum_chances", 1),
        (store_random_in_range, ":random_no", 0, ":sum_chances"),
        (try_begin), # tr93
          (val_sub, ":random_no", ":chance_move_to_home_center"),
          (lt, ":random_no", 0),
          (call_script, "script_party_set_ai_state", ":party_no", spai_holding_center, ":target_move_to_home_center"),
          (party_set_flags, ":party_no", pf_default_behavior, 1),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
        (else_try),
          (val_sub, ":random_no", ":chance_move_to_other_center"),
          (lt, ":random_no", 0),
          (call_script, "script_party_set_ai_state", ":party_no", spai_holding_center, ":target_move_to_other_center"),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
        (else_try),
          (val_sub, ":random_no", ":chance_recruit_troops"),
          (lt, ":random_no", 0),
          (call_script, "script_party_set_ai_state", ":party_no", spai_recruiting_troops, ":target_recruit_troops"),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
        (else_try),
          (val_sub, ":random_no", ":chance_raid_around_center"),
          (lt, ":random_no", 0),
          (call_script, "script_party_set_ai_state", ":party_no", spai_raiding_around_center, ":target_raid_around_center"),
          (party_set_slot, ":party_no", slot_party_commander_party, -1),
        (else_try),
          (val_sub, ":random_no", ":chance_besiege_enemy_center"),
          (lt, ":random_no", 0),
          (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, ":target_besiege_enemy_center"),
        (else_try),
          (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
		  (party_set_slot, ":party_no", slot_party_commander_party, -1),       
        (try_end), #end tr93
      (try_end), #end tr13

  ]),
]
