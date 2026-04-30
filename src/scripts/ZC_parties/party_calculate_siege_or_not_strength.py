SCRIPTS = [
("party_calculate_siege_or_not_strength",  # used by lords AI for interception factor, and in game menu instances of autoresolve
    [
      (store_script_param_1, ":party"), #Party_id
      (store_script_param_2, ":siege"),
	  
      (assign, reg(0),0),
      (party_get_num_companion_stacks, ":num_stacks",":party"),
      (assign, ":first_stack", 0),
	  
	  (try_begin),
	     (eq, ":party", "p_main_party"),
		 (assign, ":first_stack", 1),
	  (try_end),	 
	  
      (try_for_range, ":i_stack", ":first_stack", ":num_stacks"),
        (party_stack_get_troop_id,     ":stack_troop",":party",":i_stack"),
        (store_character_level, ":stack_strength", ":stack_troop"),
		
		(try_begin),            # SoD Twan change begin
		(troop_get_slot, ":trp_type", ":stack_troop", kt_slot_troop_type),
        (try_begin),
           (eq, ":siege", 1),
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
		   (else_try),
		   (eq, ":siege", 0),
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
	    (try_end), # SoD Twan change end
		
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
		
      (val_add,reg(0), ":stack_strength"),
      (try_end),
  ]),
]
