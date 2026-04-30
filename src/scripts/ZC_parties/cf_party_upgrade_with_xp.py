SCRIPTS = [
("cf_party_upgrade_with_xp",
      [
        (store_script_param_1, ":hero_party"),
        (store_script_param_2, ":amount"),
		
        #DEBUG
        (try_begin),
		  (eq, 1, 0),
          (str_store_party_name_link, s1, ":hero_party"),
          (display_message, "@Upgrading {s1}'s party...", debug_color),
        (try_end),
        #DEBUG

		(gt, ":hero_party", 0),
		(party_count_companions_of_type, ":count", ":hero_party", 0),
		(eq, ":count", 0),
		
		(assign, ":party_type", 0),
		(try_begin),
			(is_between, ":hero_party", walled_centers_begin, walled_centers_end),
			(party_get_slot, ":leader", ":hero_party", slot_town_lord),
			(assign, ":center", ":hero_party"),
			(gt, ":leader", 0),
			(store_troop_faction, ":faction", ":leader"),
			(try_begin),
				(eq, ":faction", "fac_player_supporters_faction"),
				(assign, ":party_type", 1),
			(try_end),
		(else_try),
			(party_slot_eq, ":hero_party", slot_party_type, spt_kingdom_hero_party),
			(party_stack_get_troop_id, ":leader", ":hero_party", 0),
			(party_get_attached_to, ":center", ":hero_party"),
			(store_troop_faction, ":faction", ":leader"),
			(try_begin),
				(eq, ":faction", "fac_player_supporters_faction"),
				(assign, ":party_type", 1),
			(try_end),
		(else_try),
			(assign, ":party_type", 0),
			(assign, ":leader", -1),
			(assign, ":center", "p_town_1"),
		(try_end),
		
		(try_begin),
			(eq, ":party_type", 1),
			(troop_get_slot, ":gold", ":leader", slot_troop_wealth),
		(else_try),
			(assign, ":gold", 10000),
		(try_end),
		(is_between, ":center", walled_centers_begin, walled_centers_end),
		(call_script, "script_sod_artifact_lord_doctrine_bias", ":leader"),
		(assign, ":artifact_bias", reg0),

        # ensure positive gold (negative would cause bizarre results)
		(gt, ":gold", 50),

        # make a copy of the hero party so we can iterate exclusively over that one, so our changes don't mess with our iterators...
        (call_script, "script_party_copy", "p_temp_party", ":hero_party"),

        # lets walk through the stacks in this party looking for ones to upgrade
        (party_get_num_companion_stacks, ":stacks", ":hero_party"),
		(gt, ":stacks", 1),
		(party_upgrade_with_xp, "p_temp_party", ":amount", 1),
		(try_for_range, ":i_stack", 0, ":stacks"),
			(gt, ":gold", 50),
			# only upgrade SoD* type troops
			(party_stack_get_troop_id, ":troop", ":hero_party", ":i_stack"),
			(gt, ":troop", "trp_experience_troop"),

			# get number of troops in this stack
			(party_stack_get_size, ":stack_size", ":hero_party", ":i_stack"),
			
			(try_begin),
				(troop_slot_eq, ":troop", slot_troop_sod_upgrades, 1),
				(troop_get_slot, ":upgrade1", ":troop", slot_troop_sod_upgrade1),
				(troop_get_slot, ":upgrade2", ":troop", slot_troop_sod_upgrade2),
				
				(store_random_in_range, ":upgrade1_count", 0, ":stack_size"),
				(store_sub, ":upgrade2_count", ":stack_size", ":upgrade1_count"),
			(else_try),
				(troop_get_slot, ":upgrade1", ":troop", slot_troop_sod_upgrade1),
				(assign, ":upgrade1_count", ":stack_size"),
				(assign, ":upgrade2", -1),
			(try_end),
            
			#X###########################################################################
			#UPGRADE 1
			#X###########################################################################
			
			(try_begin),
				(gt, ":upgrade1_count", 0),
				(try_begin),
					(is_between, ":center", walled_centers_begin, walled_centers_end),
					(neg|is_between, ":upgrade1", "trp_henchman", "trp_mercenaries_end"),
					(neg|is_between, ":upgrade1", "trp_farmer", "trp_black_army_fresh_blade"),
					(call_script, "script_sod_can_upgrade_troops_here", ":upgrade1", ":center"),
				(else_try),
					(assign, reg0, 1),	
				(try_end),
				(eq, reg0, 1),

				# determine how many the leader can afford to upgrade
				(call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade1", ":center"),
				(assign, ":cost", reg0),
				(val_div, ":cost", 2),
				(val_max, ":cost", 1),
				(store_div, ":can_afford", ":gold", ":cost"),

				# upgrade as many as we can afford
				(assign, ":count", ":upgrade1_count"),
				(val_min, ":count", ":can_afford"),
				(call_script, "script_sod_troop_get_elite_tier", ":upgrade1"),
				(try_begin),
					(eq, reg0, sod_elite_tier_faith),
					(store_random_in_range, ":faith_roll", 0, 100),
					(try_begin),
						(lt, ":faith_roll", 12),
						(val_min, ":count", 1),
					(else_try),
						(assign, ":count", 0),
					(try_end),
				(else_try),
					(eq, reg0, sod_elite_tier_noble),
					(store_add, ":noble_cap", 2, ":artifact_bias"),
					(val_min, ":count", ":noble_cap"),
				(try_end),

				# make sure we have something to do
				(gt, ":count", 0),

				# execute the upgrade (on the temp party, so we don't invalidate our iterators)
				(party_remove_members, "p_temp_party", ":troop", ":count"),
				(party_add_members, "p_temp_party", ":upgrade1", ":count"),

				# rack up the fees
				(val_mul, ":cost", ":count"),
				(val_sub, ":gold", ":cost"),
			(try_end),
			
			#X###########################################################################
			#UPGRADE 2
			#X###########################################################################
			
			(try_begin),
				(gt, ":gold", 50),
				(gt, ":upgrade2", 0),
				(gt, ":upgrade2_count", 0),
				(try_begin),
					(is_between, ":center", walled_centers_begin, walled_centers_end),
					(neg|is_between, ":upgrade2", "trp_henchman", "trp_mercenaries_end"),
					(neg|is_between, ":upgrade2", "trp_farmer", "trp_black_army_fresh_blade"),
					(call_script, "script_sod_can_upgrade_troops_here", ":upgrade2", ":center"),
				(else_try),
					(assign, reg0, 1),	
				(try_end),
				(eq, reg0, 1),

				# determine how many the leader can afford to upgrade
				(call_script, "script_sod_get_cost_to_upgrade_troop_at", ":upgrade2", ":center"),
				(assign, ":cost", reg0),
				(val_max, ":cost", 1),
				(store_div, ":can_afford", ":gold", ":cost"),

				# upgrade as many as we can afford
				(assign, ":count", ":upgrade2_count"),
				(val_min, ":count", ":can_afford"),
				(call_script, "script_sod_troop_get_elite_tier", ":upgrade2"),
				(try_begin),
					(eq, reg0, sod_elite_tier_faith),
					(store_random_in_range, ":faith_roll", 0, 100),
					(try_begin),
						(lt, ":faith_roll", 12),
						(val_min, ":count", 1),
					(else_try),
						(assign, ":count", 0),
					(try_end),
				(else_try),
					(eq, reg0, sod_elite_tier_noble),
					(store_add, ":noble_cap", 2, ":artifact_bias"),
					(val_min, ":count", ":noble_cap"),
				(try_end),

				# make sure we have something to do
				(gt, ":count", 0),

				# execute the upgrade (on the temp party, so we don't invalidate our iterators)
				(party_remove_members, "p_temp_party", ":troop", ":count"),
				(party_add_members, "p_temp_party", ":upgrade2", ":count"),

				# rack up the fees
				(val_mul, ":cost", ":count"),
				(val_sub, ":gold", ":cost"),

			(try_end),
        (try_end), # stacks

        # record the total remaining gold
		(try_begin),
			(eq, ":party_type", 1),
			(troop_set_slot, ":leader", slot_troop_wealth, ":gold"),
		(try_end),

        # apply the changes to actual hero party
        (call_script, "script_party_copy", ":hero_party", "p_temp_party"),
      ]
    ),
]
