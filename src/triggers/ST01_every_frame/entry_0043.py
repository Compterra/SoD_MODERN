SIMPLE_TRIGGERS = [
(0.1,
   [
    (try_for_range, ":troop_no", heroes_begin, heroes_end),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":troop_party_no", ":troop_no", slot_troop_leaded_party),
        (ge, ":troop_party_no", 1),
        (party_is_active, ":troop_party_no"),
		(party_slot_eq, ":troop_party_no", slot_party_type, spt_kingdom_hero_party), #exclude mercs
        (party_get_attached_to, ":cur_attached_town", ":troop_party_no"),
        (lt, ":cur_attached_town", 1),
        (party_get_cur_town, ":destination", ":troop_party_no"),
        (is_between, ":destination", centers_begin, centers_end),
        (call_script, "script_get_relation_between_parties", ":destination", ":troop_party_no"),
        (try_begin),
			(ge, reg0, 0),
			(party_attach_to_party, ":troop_party_no", ":destination"),
			(call_script, "script_cf_party_upgrade_with_xp", ":troop_party_no", 1),
        (else_try),
			(get_party_ai_current_behavior, ":ai_bhvr", ":troop_party_no"),
			(neq, ":ai_bhvr", ai_bhvr_hold),
			(party_set_ai_behavior, ":troop_party_no", ai_bhvr_hold),
        (try_end),
        (try_begin),
			(this_or_next|party_slot_eq, ":destination", slot_party_type, spt_town),
			(party_slot_eq, ":destination", slot_party_type, spt_castle),
			(store_faction_of_party, ":troop_faction_no", ":troop_party_no"),
			(store_faction_of_party, ":destination_faction_no", ":destination"),
			(eq, ":troop_faction_no", ":destination_faction_no"),
			(party_get_num_prisoner_stacks, ":num_stacks", ":troop_party_no"),
			(gt, ":num_stacks", 0),
			(assign, "$g_move_heroes", 1),
			(call_script, "script_party_prisoners_add_party_prisoners", ":destination", ":troop_party_no"), #Moving prisoners to the center
			(call_script, "script_party_remove_all_prisoners", ":troop_party_no"),
		   	   
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
				(neq, ":destination_faction_no", "fac_player_supporters_faction"),
                (assign, ":continue", 1),  
            (else_try),
                (assign, ":continue", 0),   				
		    (try_end),
			   
			(try_begin), #Transfer lord->center
				(eq, ":continue", 1),
			  
				(party_get_num_companions, ":num_comp_center", ":destination"),         
				(party_get_num_companions, ":num_comp_lord", ":troop_party_no"),
			 
			   	(assign, ":ideal_center_garrison", 90),
				(faction_get_slot, ":ambition", ":troop_faction_no", slot_faction_ambition),
				(val_mul, ":ambition", 5),  #twan456b
				(val_sub, ":ideal_center_garrison", ":ambition"),
			    (try_begin),
					(party_slot_eq, ":destination", slot_party_type, spt_town),
					(val_mul, ":ideal_center_garrison", 3),
			    (try_end),
			   
				(this_or_next|party_slot_eq, ":destination", slot_town_lord, ":troop_no"),
				(eq, ":troop_faction_no", "fac_kingdom_6"),			   
				(gt, ":num_comp_lord", 60),
				(gt, ":num_comp_lord", ":num_comp_center"),
				(lt, ":num_comp_center", ":ideal_center_garrison"),
				(store_sub, ":max_transfered", ":num_comp_lord", 60),
				(store_sub, ":max_transfered_2", ":ideal_center_garrison", ":num_comp_center"),
				(val_min, ":max_transfered", ":max_transfered_2"),
			   
				(gt, ":max_transfered", 0),
			   
				(assign, ":num_transfered", 0),
		       
				(party_get_num_companion_stacks, ":num_stacks", ":troop_party_no"),
		   
				(try_for_range_backwards, ":stack_no", 1, ":num_stacks"), 
				
					(lt, ":num_transfered", ":max_transfered"),		
		   
					(party_stack_get_troop_id, ":troop_id", ":troop_party_no", ":stack_no"),
					(gt, ":troop_id", -1),
					   
					(assign, ":transfer", 0),
					   
					(try_begin), 
						(this_or_next|troop_slot_eq, ":troop_id", kt_slot_troop_type, kt_troop_type_archer),   #don't let pure cavalry to guard castles
						(this_or_next|troop_slot_eq, ":troop_id", kt_slot_troop_type, kt_troop_type_footsoldier),
						(troop_slot_eq, ":troop_id", kt_slot_troop_type, kt_troop_type_mtdarcher),
						(neg|troop_is_hero, ":troop_id"),
						(party_stack_get_size, ":stack_size", ":troop_party_no", ":stack_no"),  
						(party_stack_get_num_wounded, ":num_wounded", ":troop_party_no", ":stack_no"),
						 
						(store_sub, ":transfer", ":max_transfered", ":num_transfered"),
						(val_min, ":transfer", ":stack_size"),
						(val_min, ":num_wounded", ":transfer"),
					(try_end), 	

					(try_begin), 
						(gt, ":transfer", 0),
						(party_add_members, ":destination", ":troop_id", ":transfer"),
						(party_remove_members_wounded_first, ":troop_party_no", ":troop_id", ":transfer"),
						(party_wound_members, ":destination", ":troop_id", ":num_wounded"),
						(val_add, ":num_transfered", ":transfer"),	
					(try_end), 
				(try_end), 
			(try_end),			  #twan454 end	 		 
		   
        (try_end),
    (try_end),
    ]),
]
