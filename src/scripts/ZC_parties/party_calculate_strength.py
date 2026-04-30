SCRIPTS = [
("party_calculate_strength",
    [
      (store_script_param_1, ":party"), #Party_id
      (store_script_param_2, ":exclude_leader"), #Party_id
	  
	  (party_get_attached_to, ":attached_to", ":party"),  # SoD twan
	  
	  (assign, ":siege", 0),
	  
	  (try_begin),  
      (is_between, ":party", walled_centers_begin, walled_centers_end),
      (assign, ":siege", 1),
      (else_try),	  
	  (eq, "$g_calculating_ais", 1),  # when doing the main cached strength calculation, lords use the two bonuses, then multiply their strength by 3/4
	  (assign, ":siege", 2),          # important for balance of factions power 
	  (else_try),
      (this_or_next|is_between, ":attached_to", walled_centers_begin, walled_centers_end),# siege force is used in these cases (for battles, centers and some ai calculation)
	  (party_slot_eq, ":party", slot_party_ai_state, spai_besieging_center),
	  (assign, ":siege", 1),
	  (try_end), # SOD TWan
	  
	  
      (assign, reg0,0),
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, ":first_stack", 0),
	  
      (try_begin),
        (neq, ":exclude_leader", 0),
        (assign, ":first_stack", 1),
      (try_end),
      
	  (try_for_range, ":i_stack", ":first_stack", ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (store_character_level, ":stack_strength", ":stack_troop"),
		
		(try_begin),            # SoD Twan change begin
		(ge, "$g_sod_autoresolve", 0),
		(troop_get_slot, ":trp_type", ":stack_troop", kt_slot_troop_type),
        (try_begin),
           (ge, ":siege", 1),
              (try_begin), 
              (eq, ":trp_type", kt_troop_type_cavalry),
			  (lt, ":stack_strength", 23),          # exclude the high level cavalry and heroes, who usually have good enough armors to be good in sieges
              (val_div, ":stack_strength", 5),
              (val_mul, ":stack_strength", 3),
              (else_try),
              (eq, ":trp_type", kt_troop_type_archer),
 			  (val_mul, ":stack_strength", 4),
			  (val_div, ":stack_strength", 3),
			  (else_try),
			  (eq, ":trp_type", kt_troop_type_mtdarcher),
			  (val_mul, ":stack_strength", 6),
			  (val_div, ":stack_strength", 5),
			  (else_try),
			  (eq, ":trp_type", kt_troop_type_footsoldier),   #make elite infantry like huscarls as good as archers in sieges
		      (ge, ":stack_strength", 25),
              (val_mul, ":stack_strength", 4),
              (val_div, ":stack_strength", 3),
              (try_end),  			  
		      (try_begin),
			  (le, ":stack_strength", 12),             # low level units (as well as mid level cavalry) suck in sieges out of archers
			  (lt, ":trp_type", kt_troop_type_archer),
			  (val_mul, ":stack_strength", 2),
			  (else_try),
			  (ge, ":stack_strength", 25),             # elites matter a lot in sieges last tier units bonus is increased
			  (val_mul, ":stack_strength", 4),
			  (val_div, ":stack_strength", 3),
			  (try_end),
		   (try_end),	  
		   (try_begin),
		   (neq, ":siege", 1),		   
		       (try_begin),
			   (eq, ":trp_type", kt_troop_type_cavalry),
			   (val_mul, ":stack_strength", 3),
			   (val_div, ":stack_strength", 2),
			   (else_try),
		       (eq, ":trp_type", kt_troop_type_mtdarcher),
			   (val_mul, ":stack_strength", 4),
			   (val_div, ":stack_strength", 3),
			   (else_try),
			   (le, ":stack_strength", 15),           # low and mid level units are disadvantaged only if not mounted (and not as much as in sieges) 
			   (val_mul, ":stack_strength", 4),
			   (val_div, ":stack_strength", 5),
			   (try_end),
			   (try_begin),
			   (ge, ":stack_strength", 25),          # elite are advantaged but not as much as in sieges
			   (val_mul, ":stack_strength", 5),  
			   (val_div, ":stack_strength", 4),   # some examples : swadian knight lv25 cav (native : 14 / in siege : 20 / in open battle : 34) huscarl lv28 inf (native 16, siege 38 open 16)	
			   (try_end),                         # nord footman lv10 inf ( native 5, siege 3, open 4), 
			(try_end),                 
	    (try_end),
		
		(val_add, ":stack_strength", 12),
        (val_mul, ":stack_strength", ":stack_strength"),
        (val_div, ":stack_strength", 100),
		(try_begin),
          (neg|troop_is_hero, ":stack_troop"),
          (party_stack_get_size, ":stack_size",":party",":i_stack"),
          (party_stack_get_num_wounded, ":num_wounded",":party",":i_stack"),
          (val_sub, ":stack_size", ":num_wounded"),
          (val_max, ":stack_size", 0),
          (val_mul, ":stack_strength", ":stack_size"),
        (else_try),
          (troop_is_wounded, ":stack_troop"), #hero...
          (assign,":stack_strength",0),
        (try_end),
      (val_add,reg0, ":stack_strength"),
		
      (try_end),
	  
	  	  (try_begin),
		  (eq, "$g_calculating_ais", 1),
		  (eq, "$g_sod_deactivate_ai", 0),
		  (val_mul, reg0, 4),
		  (val_div, reg0, 5),
		(try_end),  
	  
	  (try_begin),
	  (this_or_next|eq, "$g_calculating_ais", 1), # lords don't cache their strength when this script is called in battle
	  (eq, "$g_sod_autoresolve", -1),
      (party_set_slot, ":party", slot_party_cached_strength, reg0),
	  (try_end),
  ]),
]
