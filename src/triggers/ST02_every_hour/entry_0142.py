SIMPLE_TRIGGERS = [
(1,  [  #FIX FOR NEGATIVE GOLD
   
           (store_troop_gold, ":gold", "trp_player"),
   
			   (try_begin),
			   (lt, ":gold", 0),
			   (store_mul, ":add", ":gold", -1),
			   (troop_add_gold, "trp_player", ":add"),
			   (try_end),
			   
			   (try_begin),
			   (gt, "$g_player_debt_to_party_members", 1000000),
			   (assign, "$g_player_debt_to_party_members", 0),
			   (try_end),    
   
			# FIX FOR SELF WAR BUG
			
			(try_for_range, ":faction_no", kingdoms_begin, kingdoms_end), #twan456
			(store_relation, ":rln", ":faction_no", ":faction_no"),
			(lt, ":rln", 0),
			(call_script, "script_diplomacy_start_peace_between_kingdoms", ":faction_no", ":faction_no", 3),
			(set_relation, ":faction_no", ":faction_no", 100),
			(try_end),
   
            (try_for_range, ":kingdom_hero", kingdom_heroes_begin, kingdom_heroes_end),
			(neg|troop_slot_ge, ":kingdom_hero", slot_troop_prisoner_of_party, 0),
			(troop_get_slot, ":kingdom_hero_party", ":kingdom_hero", slot_troop_leaded_party),
            (gt, ":kingdom_hero_party", 0),
			(party_is_active, ":kingdom_hero_party"),
			(party_slot_eq, ":kingdom_hero_party", slot_party_type, spt_kingdom_hero_party), #twan453 exclude mercenaries
			(store_faction_of_party, ":hero_fac", ":kingdom_hero_party"),
			
			(party_get_battle_opponent, ":opponent", ":kingdom_hero_party"),

			(lt, ":opponent", 0),          # do nothing to parties in battles
			
		    (party_get_attached_to, ":attached_to", ":kingdom_hero_party"), 
			
			   (assign, ":commander", 0),
			   (assign, ":commanded", 0),
		
			   
			    (try_begin),
			      (faction_slot_eq, ":hero_fac", slot_faction_marshall, ":kingdom_hero"),
				  (assign, ":commander", 1),
			    (else_try),			   
				   (try_for_range, ":lord", kingdom_heroes_begin, kingdom_heroes_end),  # check if the lord command other lords
				   (troop_get_slot, ":lord_party", ":lord", slot_troop_leaded_party),
				   (gt, ":lord_party", 0),
				   (party_slot_eq, ":lord_party", slot_party_commander_party, ":kingdom_hero_party"),
				   (assign, ":commander", 1),
				   (try_end),	
               (try_end), 			   

			   (try_begin),
			     (neg|party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_undefined),  
				 
				 (troop_set_slot, ":kingdom_hero", slot_lord_ai_timer, 0),                   
				 (else_try),
				 (troop_get_slot, ":timer", ":kingdom_hero", slot_lord_ai_timer), # twan453 note : replace slot_lord_ai_timer with slot_lord_pursuit_state if changing slot name create save problems
				 (val_add, ":timer", 1),
				 (troop_set_slot, ":kingdom_hero", slot_lord_ai_timer, ":timer"),
               (try_end),  

		        (party_get_num_companions, ":num_comp_lord", ":kingdom_hero_party"),
			   
			   
           # Transfer Center -> Lord  twan454
		   
		   	   (try_begin),          
			   (eq, "$g_sod_deactivate_ai", 0),
		       (is_between, ":attached_to", walled_centers_begin, walled_centers_end),
		       (store_faction_of_party, ":center_fac", ":attached_to"),
			   (eq, ":hero_fac", ":center_fac"),
			   
			 (faction_get_slot, ":transfer_system", "fac_player_faction", slot_faction_center_transfer_option),#twan454 begin   
			 (try_begin),
                (this_or_next|eq, ":transfer_system", 0),
				(eq, ":transfer_system", 2),
                (eq, "$g_sod_deactivate_ai", 0),
				(assign, ":continue", 1),
                (else_try),
                (this_or_next|eq, ":transfer_system", 1),
				(eq, ":transfer_system", 3),
				(eq, "$g_sod_deactivate_ai", 0),
				(neq, ":center_fac", "fac_player_supporters_faction"),
                (assign, ":continue", 1), 
                (else_try),
                (assign, ":continue", 0),   				
		     (try_end),
			   
			(eq, ":continue", 1),   
			   
			    (party_get_num_companions, ":num_comp_center", ":attached_to"),
				
			     (call_script, "script_party_get_ideal_size", ":kingdom_hero_party"),
				 (assign, ":ideal_size", reg0),
				 
				 (assign, ":minimum_center_garrison", 100), #twan456c
				 (faction_get_slot, ":ambition", ":hero_fac", slot_faction_ambition),
				 (val_mul, ":ambition", 5),
				 (val_sub, ":minimum_center_garrison", ":ambition"),

               (try_begin), 
			   (gt, ":ideal_size", ":num_comp_lord"),
                     (try_begin),
                     (party_slot_eq, ":attached_to", slot_party_type, spt_town),
                     (val_div, ":num_comp_center", 2),
                     (try_end), 					 
		       (lt, ":num_comp_lord", 80),
			   (gt, ":num_comp_center", ":num_comp_lord"),
		       (store_sub, ":max_transfered", ":num_comp_center", 80),
			  
				  (try_begin),
					(party_slot_eq, ":attached_to", slot_town_lord, ":kingdom_hero"),
					(store_sub, ":max_transfered_2", ":ideal_size", ":num_comp_lord"),
					(else_try),
					(eq, ":hero_fac", "fac_kingdom_6"),
					(store_sub, ":max_transfered_2", 60, ":num_comp_lord"),
					(else_try),
					(neg|party_slot_eq, ":attached_to", slot_town_lord, ":kingdom_hero"),
					(store_sub, ":max_transfered_2", 25, ":num_comp_lord"),
				  (try_end),	
				  
			  (val_min, ":max_transfered", ":max_transfered_2"),
			  
			  (try_begin),
			  (neg|party_slot_ge, ":attached_to", slot_center_is_besieged_by, 0),
              (gt, ":max_transfered", 0),  			  			  
			  (assign, ":num_transfered", 0),
			  (party_detach, ":kingdom_hero_party"),
		       
			   (party_get_num_companion_stacks, ":num_stacks", ":attached_to"),
		   
					   (try_for_range_backwards, ":stack_no", 0, ":num_stacks"), # twan456 transfer ex prisoners first
						
							   (lt, ":num_transfered", ":max_transfered"),		
				   
							   (party_stack_get_troop_id, ":troop_id", ":attached_to", ":stack_no"),
							   (gt, ":troop_id", -1),
							   (neg|troop_is_hero, ":troop_id"),
							   
							   (assign, ":transfer", 0),
							   
							   (try_begin), 
								 (neg|troop_slot_eq, ":troop_id", kt_slot_troop_type, kt_troop_type_archer),   #let pure archers to guard castles
								 
								 (party_stack_get_size, ":stack_size", ":attached_to", ":stack_no"),  
								 (party_stack_get_num_wounded, ":num_wounded", ":attached_to", ":stack_no"), 
								 
								 (store_sub, ":transfer", ":max_transfered", ":num_transfered"),
								 (val_min, ":transfer", ":stack_size"),
								 (val_sub, ":transfer", ":num_wounded"),                                       #don't take wounded
							   (try_end), 
								

							   (try_begin), 
								  (gt, ":transfer", 0),
								  (party_add_members, ":kingdom_hero_party", ":troop_id", ":transfer"),
								  (party_remove_members, ":attached_to", ":troop_id", ":transfer"),
								  (val_add, ":num_transfered", ":transfer"),	
								(try_end), 
					     (try_end),
                    (party_attach_to_party, ":kingdom_hero_party", ":attached_to"),
					
					(try_begin),
					(eq, "$g_sod_debug", 1),
					(str_store_party_name, s12, ":attached_to"),
					(str_store_party_name, s13, ":kingdom_hero_party"),
					(assign, reg4, ":num_transfered"),
					(display_log_message, "@{s12} has given {reg4} troops to {s13}", debug_color),
					(try_end),
                  (try_end),  					
                (try_end),
            (try_end),			#transfer center->lord end
			 
			
		  # make sure that extremely weakened parties leave the army and return home	
		    
			(assign, ":retreat_to_center", 0),
			(assign, ":reset_behaviour", 0),
			
            (party_get_num_prisoners, ":num_pris", ":kingdom_hero_party"),  			
		  	(party_get_slot, ":relative_strength", ":kingdom_hero_party", slot_party_cached_strength),
			(val_mul, ":relative_strength", 100),
			# Safety: avoid divide-by-zero if the cached global average ever becomes 0.
			(val_max, "$g_average_lord_army_strength", 1),
			(val_div, ":relative_strength", "$g_average_lord_army_strength"),
			(val_max, ":relative_strength", 0),

			(try_begin),
			(this_or_next|lt, ":relative_strength", 20),
			(lt, ":num_comp_lord", 20),
			(lt, ":attached_to", 0), 			
			(party_set_slot, ":kingdom_hero_party", slot_party_commander_party, -1),
			(troop_get_slot, ":readiness", ":kingdom_hero", slot_troop_readiness_to_join_army),
			(val_min, ":readiness", 25),
			(troop_set_slot, ":kingdom_hero", slot_troop_readiness_to_join_army, ":readiness"),     # it's a brutal method, but as the lord AI system give bonuses as long strength is average global readiness tend to be too high
			(troop_set_slot, ":kingdom_hero", slot_troop_readiness_to_follow_orders, ":readiness"), # (I've reduced the maluses in lords script to compensate)
            (assign, ":retreat_to_center", 1),
            (try_end),					
			
		  # check for waiting bugs			
			
           (try_begin),		  
			   (party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_undefined), # first check for party not commanded
			   (party_slot_eq, ":kingdom_hero_party", slot_party_commander_party, -1),
			
               (str_store_troop_name, s11, ":kingdom_hero"),
              # (display_log_message, "@{s11} undefined AI"),			   
			
			   (try_begin),
			   	   (this_or_next|lt, ":relative_strength", 20),
			       (lt, ":num_comp_lord", 25),
				   (lt, ":attached_to", 0), 
                   (assign, ":retreat_to_center", 1),
				(else_try),
                   (gt, ":num_pris", ":num_comp_lord"),
                   (assign, ":retreat_to_center", 1),				   
			    (else_try),
				   (assign, ":reset_behaviour", 1),
                (try_end),
           
		     (else_try), 
			     (party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_undefined),  # then party following someone
                 (party_get_slot, ":commander_party", ":kingdom_hero_party", slot_party_commander_party),
                 (assign, ":valid_commander_party", 0),
                 (try_begin),
                     (eq, ":commander_party", "p_main_party"),
                     (eq, ":hero_fac", "$players_kingdom"),
                     (assign, ":valid_commander_party", 1),
                 (else_try),
                     (gt, ":commander_party", 0),
                     (party_is_active, ":commander_party"),
                     (assign, ":valid_commander_party", 1),
                 (try_end),
                     (try_begin),
                     (eq, ":valid_commander_party", 1),   # follow your commander instead of doing nothing !
					 (party_get_battle_opponent, ":commander_opponent", ":commander_party"),

                               (try_begin),
                               (this_or_next|party_slot_eq, ":commander_party", slot_party_ai_state, spai_besieging_center),
							   (ge, ":commander_opponent", 0),
							   (store_distance_to_party_from_party, ":dist", ":kingdom_hero_party", ":commander_party"),
							   (lt, ":dist", 8),
                               (assign, ":commanded", 1),  # don't change behavior if commander is sieging or fighting and close (the engine should have control)
                               (else_try),
							   (call_script, "script_party_set_ai_state", ":kingdom_hero_party", spai_accompanying_army, ":commander_party"),
                               (assign, ":commanded", 1),
							   (try_end),
							   
                      (else_try),
                     (party_set_slot, ":kingdom_hero_party", slot_party_commander_party, -1), # you don't have commander so stop believe you have one !
					 (assign, ":reset_behaviour", 1),
					  (try_end), 
					  
			  (else_try),
                 (is_between, ":attached_to", walled_centers_begin, walled_centers_end),   # then parties in centers
				 (this_or_next|party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_undefined), 
				 (party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_retreating_to_center),
                 (assign, ":reset_behaviour", 1),
                 (assign, ":retreat_to_center", -1),	# avoid retreat loop			 
              					  
            (try_end),		

			   (try_begin),
			       (eq, ":reset_behaviour", 1),               # only reset behaviour if a lord stay 8 hours undecided
				   (lt, ":timer", 8),
				   (assign, ":reset_behaviour", 0),
				(else_try),                                   # only reset behaviour if a commander or commanded stay 19 hours undecided   
	               (eq, ":reset_behaviour", 1),               # to avoid to break factions gathering forces 
				   (this_or_next|eq, ":commander", 1),        # (don't affect retreat when weakened and anti-siege hotfix)
				   (eq, ":commanded", 1),
				   (lt, ":timer", 19),
				   (assign, ":reset_behaviour", 0),				   
				(try_end), 			
												 
			# check for heroes besieging own faction or friendly centers

              (try_begin),
				   (party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_besieging_center),		
                   (party_get_slot, ":center_no", ":kingdom_hero_party", slot_party_ai_object),

					(try_begin),
                      (is_between, ":center_no", walled_centers_begin, walled_centers_end),
                      (store_faction_of_party, ":center_fac", ":center_no"),
                      (store_relation, ":relation", ":hero_fac", ":center_fac"), 
					  (this_or_next|eq, ":hero_fac", ":center_fac"),
					  (ge, ":relation", 0),
					  (eq, ":retreat_to_center", 0),
					  (assign, ":reset_behaviour", 1),   #twan453
					  (call_script, "script_village_set_state",  ":center_no", 0),
					  (else_try),
                      (neg|is_between, ":center_no", walled_centers_begin, walled_centers_end), # just in case it happens
                      (eq, ":retreat_to_center", 0),   					  
				      (assign, ":reset_behaviour", 1),
				    (try_end),
			   (try_end),		  
			   
			   # changing wrong behaviour
			   
			   (try_begin),
                    (ge, ":reset_behaviour", 1),  #twan453 	end
                    (call_script, "script_calculate_troop_ai", ":kingdom_hero"),
                    (try_begin),
                        (party_slot_eq, ":kingdom_hero_party", slot_party_ai_state, spai_undefined),
						(party_slot_eq, ":kingdom_hero_party", slot_party_commander_party, -1),
						(lt, ":relative_strength", 60),
						(neq, ":retreat_to_center", -1),
                        (assign, ":retreat_to_center", 1),
                    (try_end),
                (try_end),

               # retreating to center 				
			   
			   (try_begin),
			      (eq, ":retreat_to_center", 1),
			   
			   (assign, ":best_faction_center", -1),                    # comparing centers
			   (assign, ":best_friendly_center", -1),
			   (assign, ":compare1", 100000),
			   (assign, ":compare2", 100000),
			   
			   
			   (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
			   (store_faction_of_party, ":center_fac", ":walled_center"),
			   (store_relation, ":rln", ":center_fac", ":hero_fac"),
			   (store_distance_to_party_from_party, ":dist", ":kingdom_hero_party", ":walled_center"),

				   (try_begin),
					 (party_slot_eq, ":walled_center", slot_town_lord, ":kingdom_hero"), # big priority to owned centers
					 (val_div, ":dist", 3),
				   (try_end),
				   
				   (try_begin),
					 (party_slot_ge, ":walled_center", slot_center_is_besieged_by, 0), # avoid besieged ones unless there is nothing else
					 (val_mul, ":dist", 100),
					(try_end), 				 

				   (try_begin),
					   (eq, ":center_fac", ":hero_fac"),
					   (lt, ":dist", ":compare1"),
					   (assign, ":compare1", ":dist"),
					   (assign, ":best_faction_center", ":walled_center"),
				   (else_try),
						(ge, ":rln", 0),
						(lt, ":dist", ":compare2"),
						(assign, ":compare2", ":dist"),
						(assign, ":best_friendly_center", ":walled_center"),
					(try_end),
                (try_end),
				
				(try_begin),
				  (is_between, ":best_faction_center", walled_centers_begin, walled_centers_end), #twan 453
				  (lt, ":compare1", 60),  
				  (call_script, "script_party_set_ai_state", ":kingdom_hero_party", spai_retreating_to_center, ":best_faction_center"),
                  (else_try),
				  (is_between, ":best_friendly_center", walled_centers_begin, walled_centers_end),
				  (lt, ":compare2", ":compare1"), 
				  (call_script, "script_party_set_ai_state", ":kingdom_hero_party", spai_retreating_to_center, ":best_friendly_center"),
				  (else_try),
				  (is_between, ":best_faction_center", walled_centers_begin, walled_centers_end),
				  (call_script, "script_party_set_ai_state", ":kingdom_hero_party", spai_retreating_to_center, ":best_faction_center"),
				  (else_try),
				  (is_between, ":best_friendly_center", walled_centers_begin, walled_centers_end), #twan 453 end
				  (call_script, "script_party_set_ai_state", ":kingdom_hero_party", spai_retreating_to_center, ":best_friendly_center"),
				  (else_try),
				  (call_script, "script_party_set_ai_state", ":kingdom_hero_party", spai_undefined, -1),
				(try_end),

				(try_end),
			(try_end),	
				  
			 ]),
]
