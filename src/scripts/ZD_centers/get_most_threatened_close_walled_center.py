SCRIPTS = [
("get_most_threatened_close_walled_center",
	
	[ (store_script_param_1, ":party_no"),
      (assign, ":range", 35),
	  (assign, ":compare", 0),
	  (assign, ":most_threatened", -1),
	  
	  (store_faction_of_party, ":party_fac", ":party_no"),
	  (faction_get_slot, ":ambition", ":party_fac", slot_faction_ambition),
	  (val_mul, ":ambition", -5),
	  (val_add, ":range", ":ambition"),
	  (val_max, ":range", 20),
	  
	  (try_for_range, ":walled_center_no", walled_centers_begin, walled_centers_end),
		  (store_faction_of_party, ":center_fac", ":walled_center_no"),
		  (store_distance_to_party_from_party, ":dist", ":party_no", ":walled_center_no"),
		  (eq, ":center_fac", ":party_fac"),
		  (lt, ":dist", ":range"),
		  (call_script, "script_get_center_threat_level", ":walled_center_no"),
		  (assign, ":threat", reg0),
		  
		  (try_begin),
		  (ge, ":threat", 1),
		  
			  (try_begin),
			  (party_slot_eq, ":walled_center_no", slot_party_type, spt_town), # give priority to threatened towns
			  (val_add, ":threat", 2),		   
			  (try_end),	  
			  
				(try_for_parties, ":other_party"),
				   (party_slot_eq, ":other_party", slot_party_type, spt_kingdom_hero_party),
				   (party_slot_eq, ":other_party", slot_party_ai_state, spai_holding_center),
				   (party_slot_eq, ":other_party", slot_party_ai_object, ":walled_center_no"),
				   (neq, ":other_party", ":party_no"),
				   (val_sub, ":threat", 1),   # avoid to see all heroes in a region defend the same center
				   (val_max, ":threat", 0),	
				 (try_end), 

			  (val_add, ":threat", 2),	 
			  (val_mul, ":threat", ":threat"),			#twan456 little changes				  
		  
				 (try_begin),
				 (gt, ":threat", ":compare"),
				 (assign, ":compare", ":threat"),
				 (assign, ":most_threatened", ":walled_center_no"),
				 (try_end),
				 
		(try_end),
	(try_end),
		
		(try_begin),
		(gt, ":compare", 15),
		(else_try),
		(gt, ":compare", 0),
		(assign, ":compare", 10),
		(try_end),	
				
		(assign, reg1, ":most_threatened"), # target move to other center
		(assign, reg2, ":compare"), # chance to move to other center
	
		]),
]
