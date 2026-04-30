SCRIPTS = [
("inflict_casualties_to_party",
    [
      (party_clear, "p_temp_casualties"),
      (store_script_param_1, ":party"), #Party_id
      (call_script, "script_party_count_fit_regulars", ":party"),
      (assign, ":num_fit", reg(0)), #reg(47) = number of fit regulars.
      (store_script_param_2, ":num_attack_rounds"), #number of attacks
      (try_for_range, ":unused", 0, ":num_attack_rounds"),
        (gt, ":num_fit", 0),
        (store_random_in_range, ":attacked_troop_rank", 0 , ":num_fit"), #attack troop with rank reg(46)
        (assign, reg1, ":attacked_troop_rank"),
        (call_script, "script_get_stack_with_rank", ":party", ":attacked_troop_rank"),
        (assign, ":attacked_stack", reg(0)), #reg(53) = stack no to attack.
        (party_stack_get_troop_id,     ":attacked_troop", ":party", ":attacked_stack"),
        (store_character_level, ":troop_toughness", ":attacked_troop"),
		                    # twan new make elite better if bloodbath is used and mid level infantry a little tougher than cavalry and archers
		(troop_get_slot, ":trp_type", ":attacked_troop", kt_slot_troop_type),

        (try_begin),
			(eq, "$g_sod_autoresolve", 0),		
			(try_begin),                                     
				(le, ":troop_toughness", 10),
				(val_add, ":troop_toughness", 4),  #troop-toughness = level + 5
			(else_try),
				(this_or_next|le, ":troop_toughness", 20),
				(neq, ":trp_type", kt_troop_type_footsoldier),
				(val_add, ":troop_toughness", 5),
			(else_try),
				(lt, ":troop_toughness", 27),
				(val_add, ":troop_toughness", 6),
			(else_try),
				(store_sub, ":bonus", ":troop_toughness", 20),
				(val_min, ":bonus", 10), # don't increase level too much
				(val_add, ":troop_toughness", ":bonus"),
			(try_end),
        (else_try),
            (val_add, ":troop_toughness", 5),
        (try_end),
		(val_max, ":troop_toughness", 1),
		
		(try_begin),
		(eq, "$g_sod_autoresolve", 0),
		(store_div, ":wound_chance", ":troop_toughness", 12),	# twan new	
        (val_clamp, ":wound_chance", 1, 3),		# elites have 1/2 to be wounded, mid level 1/3, lowest levels (recruits) 1/5
		(else_try),
        (assign, ":wound_chance", 2),
        (try_end),  		
		   
        (assign, ":casualty_chance", 10000),
        (val_div, ":casualty_chance", ":troop_toughness"), #dying chance
        (try_begin),
          (store_random_in_range, ":rand_num", 0 , 10000),
          (lt, ":rand_num", ":casualty_chance"), #check chance to be a casualty
          (store_random_in_range, ":rand_num2", 0, 6), #check if this troop will be wounded or killed
          (try_begin),
            (troop_is_hero, ":attacked_troop"), #currently troop can't be a hero, but no harm in keeping this.
            (store_troop_health, ":troop_hp", ":attacked_troop"),
            (val_sub, ":troop_hp", 45),
            (val_max, ":troop_hp", 1),
            (troop_set_health, ":attacked_troop", ":troop_hp"),
          (else_try),
            (lt, ":rand_num2", ":wound_chance"), #wounded twan new
            (party_add_members, "p_temp_casualties", ":attacked_troop", 1),  # twan new end
            (party_wound_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_wound_members, ":party", ":attacked_troop", 1),
          (else_try), #killed
            (party_add_members, "p_temp_casualties", ":attacked_troop", 1),
            (party_remove_members, ":party", ":attacked_troop", 1),
          (try_end),
          (val_sub, ":num_fit", 1), #adjust number of fit regulars.
        (try_end),
      (try_end),
  ]),
]
