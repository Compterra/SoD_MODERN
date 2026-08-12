SCRIPTS = [
("game_event_simulate_battle",
    [
      (store_script_param_1, ":root_defender_party"),
      (store_script_param_2, ":root_attacker_party"),
      (assign, ":lets_recalculate_ais", 0),

      # This engine callback can arrive after a dynamic party has been removed.
      # party_is_active is the only safe way to validate a dynamic party handle
      # before store_faction_of_party or any other party operation reads it.
      (assign, ":root_parties_active", 0),
      (try_begin),
        (party_is_active, ":root_defender_party"),
        (party_is_active, ":root_attacker_party"),
        (assign, ":root_parties_active", 1),
      (try_end),

      (try_begin),
        (eq, ":root_parties_active", 1),
        (try_begin), #tr0
        (store_faction_of_party, ":defender_faction", ":root_defender_party"),
        (store_faction_of_party, ":attacker_faction", ":root_attacker_party"),
        (neq, ":defender_faction", "fac_player_faction"),
        (neq, ":attacker_faction", "fac_player_faction"),
        (store_relation, ":reln", ":defender_faction", ":attacker_faction"),
        (ge, ":reln", 0),
        (set_trigger_result, 1),
      (else_try),
        (assign, ":trigger_result", 0),

        (try_begin), #tr1
          (this_or_next|eq, "$g_battle_simulation_cancel_for_party", ":root_defender_party"),
          (eq, "$g_battle_simulation_cancel_for_party", ":root_attacker_party"),
          (assign, "$g_battle_simulation_cancel_for_party", -1),
          (assign, "$auto_enter_town", "$g_battle_simulation_auto_enter_town_after_battle"),
          (assign, ":trigger_result", 1),
        (else_try),
          (try_begin), #tr2
            (this_or_next|party_slot_eq, ":root_defender_party", slot_party_retreat_flag, 1),
            (party_slot_eq, ":root_attacker_party", slot_party_retreat_flag, 1),
            (assign, ":trigger_result", 1), #End battle!
          (try_end), #tr2
          (party_set_slot, ":root_attacker_party", slot_party_retreat_flag, 0),

          ##         (assign, ":cancel_attack", 0),

          (party_collect_attachments_to_party, ":root_defender_party", "p_collective_ally"),
          (party_collect_attachments_to_party, ":root_attacker_party", "p_collective_enemy"),
                                             ########################## SOD TWAN CHANGES BEGIN ####################################################################
          (assign, ":is_siege", 0),
           (try_begin),  #tr3           
             (this_or_next|party_slot_eq, ":root_defender_party", slot_party_type, spt_castle),
             (party_slot_eq, ":root_defender_party", slot_party_type, spt_town),
             (assign, ":is_siege", 1),
           (try_end), #tr3
           
		   (try_begin), #tr4
		   (eq, "$g_sod_autoresolve", 1), # KT0 AUTORESOLVE BEGIN
		   
           # Antigravity: Ensure AI Attackers get the Attacker siege param (2) instead of the Defender param (1)!
           (assign, ":is_siege_atk", ":is_siege"),
           (try_begin),
              (eq, ":is_siege", 1),
              (assign, ":is_siege_atk", 2),
           (try_end),

           (call_script, "script_kt_party_calculate_strength", "p_collective_ally", 0, ":is_siege"),
           (assign, ":defender_strength", reg0),
           (assign, ":defender_defense", reg1),
           (call_script, "script_kt_party_calculate_strength", "p_collective_enemy", 0, ":is_siege_atk"),
           (assign, ":attacker_strength", reg0),
           (assign, ":attacker_defense", reg1),
                                 
           # For sieges increase attacker casualties and reduce defender casualties.
           (try_begin),     #tr5        
             (this_or_next|party_slot_eq, ":root_defender_party", slot_party_type, spt_castle),
             (party_slot_eq, ":root_defender_party", slot_party_type, spt_town),
             (val_mul, ":defender_strength", 3),
             (val_div, ":defender_strength", 2),
             (val_div, ":attacker_strength", 2),
           (try_end), #tr5
                      
           # calculate damage values given average defense
           (store_mul, ":defender_adjusted_damage", ":attacker_defense", ":defender_strength"),
           (store_mul, ":attacker_adjusted_damage", ":defender_defense", ":attacker_strength"),
           (val_div, ":defender_adjusted_damage", 100),
           (val_div, ":attacker_adjusted_damage", 100),
           
           # normalize values to make battles go more slowly
           # a normal party with ~100 guys typically generates an attack 
           # value around 5000.  this should be twice what Native was
           # with the added bonus that we don't cap the upper bound.
           (val_div, ":attacker_adjusted_damage", 50),
           (val_div, ":defender_adjusted_damage", 50),
           (val_max, ":attacker_adjusted_damage", 1),
           (val_max, ":defender_adjusted_damage", 1),
           
           (try_begin),#tr6
             (inflict_casualties_to_party_group, ":root_attacker_party", ":defender_adjusted_damage", "p_temp_casualties"),
             (party_collect_attachments_to_party, ":root_attacker_party", "p_collective_enemy"),
           (try_end), #tr6
           (call_script, "script_party_count_fit_for_battle", "p_collective_enemy", 0),
           (assign, ":new_attacker_strength", reg0),

           (try_begin), #tr7
             (gt, ":new_attacker_strength", 0),
             (inflict_casualties_to_party_group, ":root_defender_party", ":attacker_adjusted_damage", "p_temp_casualties"),
             (party_collect_attachments_to_party, ":root_defender_party", "p_collective_ally"),
           (try_end), #tr7
           (call_script, "script_party_count_fit_for_battle", "p_collective_ally", 0),
           (assign, ":new_defender_strength", reg0),                                 # ########### KT0AUTORESOLVE ENDS
   
           (else_try), #tr4    # NATIVE OR BLOOD BATH AUTORESOLVE (blood bath autoresolve is 1,5 to 2 times faster than native when parties have low strength, and up to 10-12 times at extreme strengths)
		      (try_begin), #tr8
			  (eq, "$g_sod_autoresolve", -1), # native
			  (assign, ":max_str", 50), # max strength counted (after division)
			  (assign, ":div", 20), # base strength divided by
			  (assign, ":min_str_att", 1),
			  (assign, ":min_str_def", 1),
			  (else_try),
			  (eq, ":is_siege", 0),
			  (assign, ":max_str", 300),  #strength up to 10500 counted 
			  (assign, ":div", 40),
			  (assign, ":min_str_att", 2),
			  (assign, ":min_str_def", 2),
              (else_try),
              (assign, ":max_str", 200), # twan new
              (assign, ":div", 50),   # slow the average siege battles a little (at very high strength they are still extremely fast)		  
			  (assign, ":min_str_att", 2),    # but make sieges with very small forces more deadly especially for attacker
			  (assign, ":min_str_def", 5),
			  (try_end), #tr8
		   
		   (call_script, "script_party_calculate_strength", "p_collective_ally", 0),
           (assign, ":defender_strength", reg0),
#           (call_script, "script_party_count_fit_for_battle", "p_collective_enemy"),
           (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
           (assign, ":attacker_strength", reg0),
		   
		   (assign, ":attacker_rounds", 1), 
		   (assign, ":defender_rounds", 1),
		   
		   (try_begin), #tr9
		   (eq, "$g_sod_autoresolve", 0),
		   (store_mul, ":advantage_att", ":defender_strength", 3), # advantage the stronger party (+50% advantage), even if the two strengths are at the maximum
		   (val_div, ":advantage_att", 2),                         
		   (store_mul, ":advantage_def", ":attacker_strength", 3),
		   (val_div, ":advantage_def", 2),		   
		       (try_begin), #tr10
			     (eq, ":is_siege", 1),       # in sieges this advantage is harder to have for the attacker
				 (this_or_next|party_slot_eq, ":root_defender_party", slot_center_siege_with_belfry, 1),
				 (party_slot_eq, ":root_defender_party", slot_party_type, spt_town),
				 (val_mul, ":advantage_att", 2), # need to be 3vs1 to have advantage
				 (else_try),
				 (eq, ":is_siege", 1), # need to be 2,25 vs1 to have advantage
                 (val_div, ":advantage_att", 2),
				 (val_mul, ":advantage_att", 3),
               (try_end), #tr10				 
			   (try_begin),    #tr11                            
				 (gt, ":attacker_strength", ":advantage_att"),
				 (val_add, ":attacker_rounds", 1),
				(else_try),
				 (gt, ":defender_strength", ":advantage_def"),
				 (val_add, ":defender_rounds", 1),
				(try_end),  #tr11
			(val_mul, ":advantage_def", 4),
            (val_mul, ":advantage_att", 4),	
			   (try_begin),      #tr12                            # overkill level = 6x enemy strength (9 or 12x for attacker in sieges)
				 (gt, ":attacker_strength", ":advantage_att"), 
				 (val_add, ":attacker_rounds", 1),
				(else_try),
				 (gt, ":defender_strength", ":advantage_def"),
				 (val_add, ":defender_rounds", 1),
				(try_end),  		#tr12
            (try_end),	#tr9			
		   
           (store_div, ":defender_strength", ":defender_strength", ":div"),
           (val_min, ":defender_strength", ":max_str"),
           (val_max, ":defender_strength", ":min_str_def"),
           (store_div, ":attacker_strength", ":attacker_strength", ":div"),
           (val_min, ":attacker_strength", ":max_str"),
           (val_max, ":attacker_strength", ":min_str_att"),
		   
		   (try_begin), #tr13
             #For sieges increase attacker casualties and reduce defender casualties.
             (eq, ":is_siege", 1),
				 (try_begin), #tr14
				 (eq, "$g_sod_autoresolve", -1),   # native autoresolve
				 (val_mul, ":defender_strength", 3),
				 (val_div, ":defender_strength", 2),
				 (val_div, ":attacker_strength", 2),
				 (else_try),
				 (val_add, ":defender_rounds", 3),  # (instead of changing defender strength they inflict 3 or 4 times their casualties for 1 or 2 of the attacker)
				 (val_div, ":attacker_strength", 3), # attackers still have a strength malus in addition (sieges succeeded a little too often without)
				 (val_mul, ":attacker_strength", 2),
				 (try_end), #tr14
		   (else_try),
		     (eq, "$g_sod_autoresolve", 0),
			 (val_add, ":attacker_rounds", 1),
			 (val_add, ":defender_rounds", 1),
           (try_end), #tr13

		   (try_begin),  	#tr15		 
			 (is_currently_night),
			 (val_sub, ":attacker_rounds", 1),
			 (val_sub, ":defender_rounds", 1),
             (val_min, ":defender_rounds", 2),
		  (try_end),	 #tr15

			(assign, ":new_defender_strength", 1), # avoid the system to think the battle has ended in first round
			(assign, ":new_attacker_strength", 1),
          
		  (try_for_range, ":unused", 0, 5), #tr16       # allow 5 rounds maximum (defender overkill + siege don't advantage him more) 
            (val_sub, ":attacker_rounds", 1),      
            (val_sub, ":defender_rounds", 1),    
			
              (try_begin), #tr17
              (ge, ":defender_rounds", 0),	
              (gt, ":new_defender_strength", 0),
              (gt, ":new_attacker_strength", 0),			  
              (inflict_casualties_to_party_group, ":root_attacker_party", ":defender_strength", "p_temp_casualties"),
              (party_collect_attachments_to_party, ":root_attacker_party", "p_collective_enemy"),
              (try_end), #tr17

		   (call_script, "script_party_count_fit_for_battle", "p_collective_enemy", 0),
           (assign, ":new_attacker_strength", reg0),

    		   (try_begin), #tr18
				 (gt, ":new_attacker_strength", 0),
				 (gt, ":new_defender_strength", 0),
				 (ge, ":attacker_rounds", 0), 
				 (inflict_casualties_to_party_group, ":root_defender_party", ":attacker_strength", "p_temp_casualties"),
				 (party_collect_attachments_to_party, ":root_defender_party", "p_collective_ally"),
			   (try_end), #tr18
			   
           (call_script, "script_party_count_fit_for_battle", "p_collective_ally", 0),
           (assign, ":new_defender_strength", reg0),      

          (try_end), #tr16 end rounds		   
                                
	(try_end), #tr4			 ################### TWAN AUTORESOLVE END ##########################################################				 
		   
          (try_begin), #tr19
            (this_or_next|eq, ":new_attacker_strength", 0),
            (eq, ":new_defender_strength", 0),
            # Battle concluded! determine winner

            (try_begin), #tr20
              (eq, ":new_attacker_strength", 0),
              (eq, ":new_defender_strength", 0),
              (assign, ":root_winner_party", -1),
              (assign, ":root_defeated_party", -1),
              (assign, ":collective_casualties", -1),
            (else_try),
              (eq, ":new_attacker_strength", 0),
              (assign, ":root_winner_party",   ":root_defender_party"),
              (assign, ":root_defeated_party", ":root_attacker_party"),
              (assign, ":collective_casualties",    "p_collective_enemy"),
            (else_try),
              (assign, ":root_winner_party", ":root_attacker_party"),
              (assign, ":root_defeated_party",  ":root_defender_party"),
              (assign, ":collective_casualties",  "p_collective_ally"),
            (try_end), #tr20

            (try_begin), #tr21
              (ge, ":root_winner_party", 0),
              (call_script, "script_sod_party_record_lord_battle_outcome", ":root_winner_party", 1),
              (call_script, "script_sod_party_record_lord_battle_outcome", ":root_defeated_party", -1),
              (call_script, "script_sod_merc_lord_note_battle_outcome", ":root_winner_party", 1),
              (call_script, "script_sod_merc_lord_note_battle_outcome", ":root_defeated_party", -1),
              (call_script, "script_sod_black_khergits_note_ai_battle_outcome", ":root_winner_party", ":root_defeated_party"),
              (call_script, "script_get_nonempty_party_in_group", ":root_winner_party"),
              (assign, ":nonempty_winner_party", reg0),
              (store_faction_of_party, ":faction_receiving_prisoners", ":nonempty_winner_party"),
              (store_faction_of_party, ":defeated_faction", ":root_defeated_party"),
            (else_try),
              (assign, ":nonempty_winner_party", -1),
            (try_end), #tr21

            (try_begin), #tr22
              (ge, ":collective_casualties", 0),
              (party_get_num_companion_stacks, ":num_stacks", ":collective_casualties"),
            (else_try),
              (assign, ":num_stacks", 0),
            (try_end), #tr22
			
            (try_for_range, ":troop_iterator", 0, ":num_stacks"), #tr23
              (party_stack_get_troop_id, ":cur_troop_id", ":collective_casualties", ":troop_iterator"),
              (troop_is_hero, ":cur_troop_id"),
              (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
              (troop_set_slot, ":cur_troop_id", slot_troop_leaded_party, -1),
              (store_random_in_range, ":rand", 0, 100),
              (call_script, "script_store_troop_name_link", s1, ":cur_troop_id"),
              (str_store_faction_name_link, s2, ":faction_receiving_prisoners"),
              (store_troop_faction, ":defeated_troop_faction", ":cur_troop_id"),
              (str_store_faction_name_link, s3, ":defeated_troop_faction"),
				  (try_begin), #tr24
					(party_stack_get_troop_id, ":leader_troop_id", ":nonempty_winner_party", 0),
					(is_between, ":leader_troop_id", kingdom_heroes_begin, kingdom_heroes_end),
					(call_script, "script_cf_check_hero_can_die_in_battle", ":cur_troop_id"),
					(display_message, "@{s1} of {s3} has died in battle against {s2}.", trivia_color),
					(call_script, "script_kill_kingdom_hero", ":cur_troop_id"),
				  (else_try),
					(ge, ":rand", hero_escape_after_defeat_chance),
					(party_stack_get_troop_id, ":leader_troop_id", ":nonempty_winner_party", 0),
					(is_between, ":leader_troop_id", kingdom_heroes_begin, kingdom_heroes_end), #disable non-kingdom parties capturing enemy lords
					(party_add_prisoners, ":nonempty_winner_party", ":cur_troop_id", 1),
					(gt, reg0, 0),
					#(troop_set_slot, ":cur_troop_id", slot_troop_is_prisoner, 1),
					(troop_set_slot, ":cur_troop_id", slot_troop_prisoner_of_party, ":nonempty_winner_party"),
					(faction_get_slot, ":weariness", ":defeated_troop_faction", slot_faction_diplomacy_war_weariness),
					(val_add, ":weariness", 2),
					(val_clamp, ":weariness", 0, 101),
					(faction_set_slot, ":defeated_troop_faction", slot_faction_diplomacy_war_weariness, ":weariness"),
					(party_stack_get_troop_id, ":leader_troop_id", ":nonempty_winner_party", 0),
					(call_script, "script_sod_artifact_capture_spoils", ":leader_troop_id", ":cur_troop_id"),
						(try_begin), #tr25
						  (eq, "$g_sod_hide_messages", 0),
						  (display_log_message, "str_hero_taken_prisoner", trivia_color),
						(try_end), #tr25
					(else_try),
						(try_begin), #tr26
						  (eq, "$g_sod_hide_messages", 0),
						  (display_message, "@{s1} of {s3} was defeated in battle but managed to escape.", trivia_color),
						(try_end), #tr26
				   (try_end), #tr24
              (try_begin), #tr27
                (store_troop_faction, ":cur_troop_faction", ":cur_troop_id"),
                (faction_slot_eq, ":cur_troop_faction", slot_faction_marshall, ":cur_troop_id"),
                #Marshall is defeated, refresh ai.
                (assign, ":lets_recalculate_ais", 1),
              (try_end), #tr27
            (try_end), #tr23
			
            (try_begin), #tr28
              (ge, ":collective_casualties", 0),
              (party_get_num_prisoner_stacks, ":num_stacks", ":collective_casualties"),
            (else_try),
              (assign, ":num_stacks", 0),
            (try_end), #tr28
			
            (try_for_range, ":troop_iterator", 0, ":num_stacks"), #tr29
              (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":collective_casualties", ":troop_iterator"),
              (troop_is_hero, ":cur_troop_id"),
              (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
              (store_troop_faction, ":cur_troop_faction", ":cur_troop_id"),
              (call_script, "script_store_troop_name_link", s1, ":cur_troop_id"),
              (str_store_faction_name_link, s2, ":faction_receiving_prisoners"),
              (str_store_faction_name_link, s3, ":cur_troop_faction"),
				  (try_begin), #tr30
					(eq, "$g_sod_hide_messages", 0),
					(display_log_message, "str_hero_freed", trivia_color),
				  (try_end), #tr30
            (try_end), #tr29

            (try_begin), #tr31
              (ge, ":collective_casualties", 0),
              (party_clear, "p_temp_party"),
              (assign, "$g_move_heroes", 0), #heroes are already processed above. Skip them here.
              (call_script, "script_party_add_party_prisoners", "p_temp_party", ":collective_casualties"),
              (call_script, "script_party_prisoners_add_party_companions", "p_temp_party", ":collective_casualties"),
              (distribute_party_among_party_group, "p_temp_party", ":root_winner_party"),
              (try_begin),
                (gt, ":nonempty_winner_party", 0),
                (neq, ":nonempty_winner_party", "p_main_party"),
                (assign, ":prisoner_train_reason", 1),
                (try_begin),
                  (faction_get_slot, ":faction_marshall", ":faction_receiving_prisoners", slot_faction_marshall),
                  (is_between, ":faction_marshall", kingdom_heroes_begin, kingdom_heroes_end),
                  (troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
                  (eq, ":nonempty_winner_party", ":faction_marshall_party"),
                  (call_script, "script_sod_marshal_get_planning_profile_to_regs", ":faction_marshall"),
                  (assign, ":marshal_logistics", reg2),
                  (ge, ":marshal_logistics", 45),
                  (assign, ":prisoner_train_reason", 28),
                (try_end),
                (call_script, "script_sod_maybe_create_prisoner_train_from_party", ":nonempty_winner_party", ":faction_receiving_prisoners", ":prisoner_train_reason", sod_prisoner_train_purpose_imprisonment),
              (try_end),
              (try_begin),
                (party_slot_ge, ":root_defeated_party", slot_party_sod_looter_raid_state, sod_looter_raid_state_moving_to_target),
                (call_script, "script_sod_looter_resolve_village_raid", ":root_defeated_party", 2),
              (try_end),
              (try_begin),
                (party_slot_eq, ":root_defeated_party", slot_party_sod_messenger_role, sod_messenger_role_tax_courier),
                (call_script, "script_sod_tax_courier_resolve_defeated_by_party", ":root_defeated_party", ":nonempty_winner_party"),
              (try_end),
              (try_begin),
                (party_slot_eq, ":root_defeated_party", slot_party_type, spt_prisoner_train),
                (call_script, "script_sod_prisoner_train_destroyed", ":root_defeated_party", ":faction_receiving_prisoners"),
              (try_end),
              (try_begin),
                (party_slot_eq, ":root_defeated_party", slot_party_sod_support_type, sod_support_type_castle_patrol),
                (call_script, "script_sod_castle_patrol_destroyed", ":root_defeated_party"),
              (try_end),
              (try_begin),
                (party_slot_eq, ":root_defeated_party", slot_party_sod_threat_active_quest, "qst_regional_threat_contract"),
                (call_script, "script_sod_threat_board_note_party_defeated", ":root_defeated_party"),
              (try_end),
              (call_script, "script_clear_party_group", ":root_defeated_party"),
              #PATROLS START
              (call_script, "script_cf_fix_party_size", "p_temp_party", 0),
              #PATROLS END
            (try_end), #tr31
            (assign, ":trigger_result", 1), #End battle!

            #Center captured
            (try_begin), #tr32
              (ge, ":collective_casualties", 0),
              (party_get_slot, ":cur_party_type", ":root_defeated_party", slot_party_type),
              (this_or_next|eq, ":cur_party_type", spt_town),
              (eq, ":cur_party_type", spt_castle),		
		      (assign, ":lets_recalculate_ais", 1),			  

              (store_faction_of_party, ":winner_faction", ":root_winner_party"),
              (store_faction_of_party, ":defeated_faction", ":root_defeated_party"),
              (faction_get_slot, ":weariness", ":defeated_faction", slot_faction_diplomacy_war_weariness),
              (val_add, ":weariness", 8),
              (val_clamp, ":weariness", 0, 101),
              (faction_set_slot, ":defeated_faction", slot_faction_diplomacy_war_weariness, ":weariness"),

              (str_store_party_name_link, s1, ":root_defeated_party"),
              (str_store_faction_name_link, s2, ":winner_faction"),
              (str_store_faction_name_link, s3, ":defeated_faction"),
              (try_begin), #tr33
                (eq, "$g_sod_hide_messages", 0),
                (display_log_message, "str_center_captured", important_color),
              (try_end), #tr33

              (try_begin), #tr34
                (eq, "$g_encountered_party", ":root_defeated_party"),
                (call_script, "script_add_log_entry", logent_player_participated_in_siege, "trp_player",  "$g_encountered_party", 0, "$g_encountered_party_faction"),
              (try_end), #tr34

              (try_begin), #tr35
                (party_get_num_companion_stacks, ":num_stacks", ":root_winner_party"),
                (gt, ":num_stacks", 0),
                (party_stack_get_troop_id, ":leader_troop_no", ":root_winner_party", 0),
                (is_between, ":leader_troop_no", kingdom_heroes_begin, kingdom_heroes_end),
                (party_set_slot, ":root_defeated_party", slot_center_last_taken_by_troop, ":leader_troop_no"),
              (else_try),
                (party_set_slot, ":root_defeated_party", slot_center_last_taken_by_troop, -1),
              (try_end), #tr35

              (call_script, "script_give_center_to_faction", ":root_defeated_party", ":winner_faction"), #twan454 should be final fix for siege bugs
			  (call_script, "script_cf_reinforce_party", ":root_defeated_party"),
              (call_script, "script_cf_reinforce_party", ":root_defeated_party"),
			  
			  (call_script, "script_order_best_besieger_party_to_guard_center", ":root_defeated_party", ":winner_faction"), 

			 (faction_get_slot, ":transfer_system", "fac_player_faction", slot_faction_center_transfer_option),#twan454 begin   
			 (try_begin),
                (this_or_next|eq, ":transfer_system", 0),
				(eq, ":transfer_system", 2),
                (eq, "$g_sod_deactivate_ai", 0),
				(assign, ":transfer_troops", 1),
                (else_try),
                (this_or_next|eq, ":transfer_system", 1),
				(eq, ":transfer_system", 3),
				(eq, "$g_sod_deactivate_ai", 0),
				(neq, ":winner_faction", "fac_player_supporters_faction"),
                (assign, ":transfer_troops", 1),
                (else_try),
                (assign, ":transfer_troops", 0),				
		     (try_end),
			  
			  (assign, ":max_garrison", 80),
			  (try_begin),
			    (eq, ":cur_party_type", spt_town),
				(assign, ":max_garrison", 150),
			  (try_end),	
			  
			  (party_get_num_companions, ":center_comp", ":root_defeated_party"),
			  (val_sub, ":max_garrison", ":center_comp"),
			  
			  (assign, ":num_transfered", 0),
			  
			  (try_for_parties, ":party_no"), #tr36
			   (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
			   (party_slot_eq, ":party_no", slot_party_ai_object, ":root_defeated_party"),
			    (store_faction_of_party, ":party_fac", ":party_no"),
			    (store_distance_to_party_from_party, ":dist", ":party_no", ":root_defeated_party"),
					    (try_begin), #tr36a
						  (eq, ":party_fac", ":winner_faction"),	
                          (lt, ":dist", 3),  						 
						  (party_attach_to_party, ":party_no", ":root_defeated_party"),
						     
						 (try_begin), #tr36b
							 (eq, "$g_sod_deactivate_ai", 0),
							 (eq, ":transfer_troops", 1),

							 (party_get_num_companions, ":num_comp", ":party_no"),
							 
							   (try_begin), #tr36c
							     (is_between, ":num_comp", 31, 65),
								 (store_sub, ":max_transfered", ":num_comp", 30),
								 (val_min, ":max_transfered", 5),
								 (else_try),
								 (is_between, ":num_comp", 65, 100),
								 (assign, ":max_transfered", 10),
								 (else_try),
								 (gt, ":num_comp", 100),
								 (assign, ":max_transfered", 15),
								 (else_try),
								 (assign, ":max_transfered", 0),
							   (try_end),	 #tr36c
							   
							     (val_min, ":max_transfered", ":max_garrison"),
								 (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
							   
						       (try_begin), #tr36d  #troop transfer begin
							     (gt, ":max_transfered", 0),
								 (gt, ":num_stacks", 1),
								 (assign, ":num_transfered", 0),
								   
								   (try_for_range, ":stack_no", 1, ":num_stacks"), #tr36e 
									
									   (lt, ":num_transfered", ":max_garrison"),				   
									   (party_stack_get_troop_id, ":troop_id", ":party_no", ":stack_no"),
									   (gt, ":troop_id", 0),
									   
									   (assign, ":transfer", 0),
									   
									   (try_begin), #tr36f
										 (this_or_next|troop_slot_eq, ":troop_id", kt_slot_troop_type, kt_troop_type_archer),   #don't let pure cavalry to guard castles
										 (this_or_next|troop_slot_eq, ":troop_id", kt_slot_troop_type, kt_troop_type_footsoldier),
										 (troop_slot_eq, ":troop_id", kt_slot_troop_type, kt_troop_type_mtdarcher),
										 (neg|troop_is_hero, ":troop_id"),
										 (party_stack_get_size, ":stack_size", ":party_no", ":stack_no"),  
										 (party_stack_get_num_wounded, ":num_wounded", ":party_no", ":stack_no"),
										 
										 (store_sub, ":transfer", ":max_garrison", ":num_transfered"),
										 (val_min, ":transfer", ":stack_size"),
										 (val_min, ":transfer", ":max_transfered"),
										 (val_min, ":num_wounded", ":transfer"),
									   (try_end), #tr36f

									   (try_begin), #tr36g
										  (gt, ":transfer", 0),
										  (party_add_members, ":root_defeated_party", ":troop_id", ":transfer"),
										  (party_remove_members_wounded_first, ":party_no", ":troop_id", ":transfer"),
										  (party_wound_members, ":root_defeated_party", ":troop_id", ":num_wounded"),
										  (val_add, ":num_transfered", ":transfer"), 
                                          (val_sub, ":max_transfered", ":transfer"), 										  
										(try_end), #tr36g
                                    (try_end),	#tr36e									
						         (try_end), #tr36d #troop transfer end
						                
						  
						     (party_get_num_prisoner_stacks, ":num_stacks", ":party_no"), #prisoner_transfers
						     (store_random_in_range, ":rnd", 0, 3),
							 (eq, ":rnd", 0),
                             (gt, ":num_stacks", 0),
                             (assign, "$g_move_heroes", 0), # just keep heroes to let them in stronger centers
                             (call_script, "script_party_prisoners_add_party_prisoners", ":root_defeated_party", ":party_no"), #move other prisoners to the conquered center
                             (assign, "$g_move_heroes", 0),
                             (call_script, "script_party_remove_all_prisoners", ":party_no"),
						  
						  (try_end), #tr36b
						 (try_end), #tr36a 
				(party_set_slot, ":party_no", slot_party_ai_state, spai_undefined),
				(party_set_ai_behavior, ":party_no", ai_bhvr_hold),
		       (try_end), #tr36
			   
			    (party_set_slot, ":root_defeated_party", slot_village_state, 0), 
				(call_script, "script_lift_siege", ":root_defeated_party", 0),


 #twan454 end	
			  
                (try_begin), #tr37
                (eq, ":defeated_faction", "fac_player_supporters_faction"),
                (call_script, "script_add_notification_menu", "mnu_notification_center_lost", ":root_defeated_party", ":winner_faction"),
					(try_begin),  #tr38                                                           # Sod Twan - Badboy Effect
					(party_slot_eq, ":root_defeated_party", slot_party_type, spt_town),
					(call_script, "script_change_badboy_rating", -8),
					(else_try),
					(party_slot_eq, ":root_defender_party", slot_party_type, spt_castle),
					(call_script, "script_change_badboy_rating", -4),
					(try_end), #tr38
				(else_try),
					(eq, ":winner_faction", "fac_player_supporters_faction"),
					(try_begin),  #tr39
					(party_slot_eq, ":root_defeated_party", slot_party_type, spt_town),
					(call_script, "script_change_badboy_rating", 10),
					(else_try),
					(party_slot_eq, ":root_defender_party", slot_party_type, spt_castle),
					(call_script, "script_change_badboy_rating", 4),                          
					(try_end), #tr39
                (try_end), 	#tr37	
				
				# Sod Twan - Badboy effect end
              #Reduce prosperity of the center by 5
              (call_script, "script_change_center_prosperity", ":root_defeated_party", -5),
			  
            (try_end), #tr32
          (try_end), #tr19

          #ADD XP
          (try_begin), #tr40
            (party_slot_eq, ":root_attacker_party", slot_party_type, spt_kingdom_hero_party),
            (store_random_in_range, ":random_num", 0, 100),
            (lt, ":random_num", 25),
            (gt, ":new_attacker_strength", 0),
            (call_script, "script_cf_party_upgrade_with_xp", ":root_attacker_party", 1000),
          (try_end), #tr40
		  
          (try_begin), #tr41
            (party_slot_eq, ":root_defender_party", slot_party_type, spt_kingdom_hero_party),
            (store_random_in_range, ":random_num", 0, 100),
            (lt, ":random_num", 25),
            (gt, ":new_defender_strength", 0),
            (call_script, "script_cf_party_upgrade_with_xp", ":root_defender_party", 1000),
          (try_end), #tr41

          (store_random_in_range, ":random_num", 0, 100),
		  
          (try_begin), #tr42
            (lt, ":random_num", 10),
            ##           (this_or_next|lt, ":random_num", 10),
            ##           (eq, ":cancel_attack", 1),
            (assign, ":trigger_result", 1), #End battle!
          (try_end), #tr42
		  
        (try_end), #tr1
          (set_trigger_result, ":trigger_result"),
        (try_end), #tr0
      (else_try),
        # A removed root party cannot be simulated. End the stale battle cleanly.
        (set_trigger_result, 1),
      (try_end),

	  (try_begin),
	    (eq, ":lets_recalculate_ais", 1),
		(assign, "$g_recalculate_ais", 1),
	  (try_end), 	
	  
  ]),
]
