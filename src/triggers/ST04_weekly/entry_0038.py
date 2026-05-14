SIMPLE_TRIGGERS = [
(24 * 7,
    [
	(try_for_range, ":center_no", centers_begin, centers_end),
		# only villages and towns are based on taxes
		(neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),

		(assign, ":cur_rents", 0),
		(assign, ":town_services", 0),
		(assign, ":town_liquidity", 0),
		(assign, ":town_tax_reliability", 100),
		(assign, ":tax_extraction_revenue_pct", 100),
		(assign, ":tax_extraction_pressure", 0),
		(assign, ":tax_wealth_drift", 0),
		(party_get_slot, ":center_population", ":center_no", slot_center_sod_local_population),
		(str_store_party_name_link, s2, ":center_no"),
		# Safety: population should never be negative (data corruption / bad math elsewhere).
		(val_max, ":center_population", 0),

		(try_begin),
			# village ...in a normal state
			(party_slot_eq, ":center_no", slot_party_type, spt_village),
			(party_slot_eq, ":center_no", slot_village_state, svs_normal),

			# taxes = 1x population for villages
			(assign, ":cur_rents", ":center_population"),
		(else_try),
			# town
			(party_slot_eq, ":center_no", slot_party_type, spt_town),

			# taxes = 1x population for towns
			(assign, ":cur_rents", ":center_population"),
			(call_script, "script_sod_get_town_market_profile", ":center_no"),
			(assign, ":town_services", reg4),
			(assign, ":town_liquidity", reg6),
			(assign, ":town_tax_reliability", reg9),
		(try_end),

		(call_script, "script_sod_get_center_tax_extraction_profile", ":center_no"),
		(assign, ":tax_extraction_revenue_pct", reg0),
		(assign, ":tax_extraction_pressure", reg1),
		(assign, ":tax_wealth_drift", reg6),

		# Productive population matters, not just raw headcount.
		# A shared capacity profile keeps tax behavior aligned with recruitment,
		# construction, food, and recovery.
		(try_begin),
			(gt, ":cur_rents", 0),
			(call_script, "script_sod_get_center_population_capacity_profile", ":center_no"),
			(assign, ":tax_capacity_pct", reg3),
			(assign, ":ideal_population", reg7),
			(val_max, ":ideal_population", 1),
			(try_begin),
				# Population above capacity still pays tax, but overcrowded centers
				# are harder to administer efficiently.
				(gt, ":center_population", ":ideal_population"),
				(store_sub, ":overcrowding", ":center_population", ":ideal_population"),
				(store_mul, ":overcrowding_pct", ":overcrowding", 100),
				(val_div, ":overcrowding_pct", ":ideal_population"),
				(store_div, ":overcrowding_tax_drag", ":overcrowding_pct", 4),
				(val_sub, ":tax_capacity_pct", ":overcrowding_tax_drag"),
				(val_max, ":tax_capacity_pct", 60),
			(try_end),
			(val_mul, ":cur_rents", ":tax_capacity_pct"),
			(val_div, ":cur_rents", 100),
		(try_end),

		# get a prosperity multiplier (0...100)
		(party_get_slot, ":multiplier", ":center_no", slot_town_prosperity),

		# catch bad prosperity
		(try_begin),
			(le, ":multiplier", 0),
			(assign, reg0, ":multiplier"),
			(try_begin),
				(eq, "$g_sod_debug", 1),
				(display_message, "@DEBUG: Prosperity for {s2} is out of bounds! ({reg0})", red),
			(try_end),
			(val_max, ":multiplier", 1),
			# fix it
			(party_get_slot, ":old_prosperity", ":center_no", slot_town_prosperity),
			(store_sub, ":prosperity_delta", ":multiplier", ":old_prosperity"),
			(call_script, "script_change_center_prosperity", ":center_no", ":prosperity_delta"),
		(try_end),
		
		#modify productivity by population health
		(party_get_slot, ":health", ":center_no", slot_center_sod_local_health),
		(val_add, ":health", 100),
		# Safety: health factor is applied as a percent multiplier; never allow negative.
		(val_max, ":health", 0),
		(val_mul, ":multiplier", ":health"),
		(val_div, ":multiplier", 100),

		(try_begin),
			# modify by faith & tax level only for the player
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(store_faction_of_party, ":center_faction", ":center_no"),
			(party_get_slot, ":faith", ":center_no", slot_center_sod_local_faith),
			(val_div, ":faith", 10),
			(val_add, ":multiplier", ":faith"),
			(try_begin),
				(party_slot_eq, ":center_no", slot_party_type, spt_village),
				(faction_get_slot, ":law_tax", ":center_faction", slot_faction_law_tax_peasants),
				(val_add, ":multiplier", ":law_tax"),
			(else_try),
				(party_slot_eq, ":center_no", slot_party_type, spt_town),
				(faction_get_slot, ":law_tax", ":center_faction", slot_faction_law_tax_townspeople),
				(val_add, ":multiplier", ":law_tax"),
				(faction_get_slot, ":badboy", "fac_player_supporters_faction", slot_faction_badboy_rating), #twan456 Badboy Malus for town income
				(try_begin),
				  (lt, ":badboy", 15),
				  (store_sub, ":badboy_multiplier", 15, ":badboy"),
				  (val_add, ":multiplier", ":badboy_multiplier"),
				(else_try),
				  (gt, ":badboy", 24),
				  (store_sub, ":badboy_multiplier", ":badboy", 25),
				  (val_sub, ":multiplier", ":badboy_multiplier"),
				(try_end),                                                         #twan456 end
			(try_end),
		(try_end),
		(try_begin),
			# Centers that reject the current legal order resist collectors; loyal centers pay more smoothly.
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(call_script, "script_sod_law_calculate_center_tax_compliance", ":center_no"),
			(assign, ":law_tax_compliance", reg0),
			(val_mul, ":multiplier", ":law_tax_compliance"),
			(val_div, ":multiplier", 100),
		(try_end),
		#building modifiers
		(try_begin),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(assign, ":mill_income_multiplier", "$g_sod_building_mill_income"),
			(assign, ":monastery_income_multiplier", "$g_sod_building_monastery_income"),
			(assign, ":guild_income_multiplier", "$g_sod_building_guild_income"),
		(else_try),
			(assign, ":mill_income_multiplier", 10),
			(assign, ":monastery_income_multiplier", 5),
			(assign, ":guild_income_multiplier", 10),
		(try_end),
		
		(try_begin),
			(party_slot_eq, ":center_no", slot_center_has_mill, 1),
			(val_add, ":multiplier", ":mill_income_multiplier"),
		(try_end),
		(try_begin),
			(party_slot_eq, ":center_no", slot_center_has_monastery, 1),
			(val_add, ":multiplier", ":monastery_income_multiplier"),
		(try_end),
		(try_begin),
			(party_slot_eq, ":center_no", slot_center_has_guild, 1),
			(val_add, ":multiplier", ":guild_income_multiplier"),
		(try_end),

        #DEBUG - CATCH BAD FAITH / GLOBAL TAX RATE
        (try_begin),
           (le, ":multiplier", 0),
         # (assign, reg0, ":multiplier"),
         #  (display_message, "@DEBUG: Faith+TaxRate for {s2} is less or equal zero! ({reg0})", red), #twan456
           (val_max, ":multiplier", 1),
        (try_end),

        # Safety clamp: :multiplier is a percent applied to rents.
        # In normal play it should stay near ~1..200, but extreme mod/law combos can push it far higher.
        # Keep it bounded to avoid runaway tax values and potential integer overflow.
        (try_begin),
          (gt, ":multiplier", 300),
          (try_begin),
            (eq, "$g_sod_debug", 1),
            (assign, reg0, ":multiplier"),
            (display_message, "@DEBUG: Tax multiplier clamped for {s2} ({reg0} -> 300)", debug_color),
          (try_end),
          (assign, ":multiplier", 300),
        (try_end),
		
		(val_mul, ":cur_rents", ":multiplier"),
        (val_div, ":cur_rents", 100),
		# Extractive tax policy buys short-term revenue with long-term pressure.
		(val_mul, ":cur_rents", ":tax_extraction_revenue_pct"),
        (val_div, ":cur_rents", 100),
		(try_begin),
			# Towns tax services, workshops, and liquid exchange, not just heads.
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			(store_mul, ":service_rents", ":town_services", 12),
			(store_div, ":liquidity_rents", ":town_liquidity", 8),
			(val_add, ":cur_rents", ":service_rents"),
			(val_add, ":cur_rents", ":liquidity_rents"),
			(val_mul, ":cur_rents", ":town_tax_reliability"),
			(val_div, ":cur_rents", 100),
			(store_div, ":market_wealth_growth", ":town_liquidity", 5),
			(val_clamp, ":market_wealth_growth", 0, 1201),
			(call_script, "script_sod_change_center_wealth", ":center_no", ":market_wealth_growth"),
		(try_end),
		(try_begin),
			(neq, ":tax_wealth_drift", 0),
			(call_script, "script_sod_change_center_wealth", ":center_no", ":tax_wealth_drift"),
			(try_begin),
				(gt, ":tax_extraction_pressure", 40),
				(call_script, "script_sod_change_center_local_prosperity", ":center_no", -1),
			(try_end),
		(try_end),
		  
		#demesne size
		(try_begin),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(assign, ":bouns_rents", ":cur_rents"),
			(call_script, "script_get_player_administration_multiplier"),
			# Safety: script returns a percent delta; clamp extreme outputs to avoid nonsense.
			(val_clamp, reg0, -100, 301),
			(val_mul, ":bouns_rents", reg0),
			(val_div, ":bouns_rents", 100),
			(val_add, ":cur_rents", ":bouns_rents"),
			# Safety: taxes should not go negative.
			(val_max, ":cur_rents", 0),
		(try_end),
		  
		#Scoutage
		(try_begin),
			(party_get_slot, ":town_lord", ":center_no", slot_town_lord),
			(is_between, ":town_lord", "trp_reserved_knight_1",  "trp_knight_6_01"),
			(eq, "$g_sod_king", 1),
			(store_troop_faction, ":town_lord_faction", ":town_lord"),
			(eq, ":town_lord_faction", "fac_player_supporters_faction"),
			#base is 30%
			(assign, ":multiplier", 30),
			#tax_nobles is modified by laws and these are not big values
			(val_mul, ":multiplier", "$g_sod_tax_nobles"),
			(val_div, ":multiplier", 100),
			(neq, ":multiplier", 0),
			#Counting taxes fromroyal tribute once again
			(assign, ":cur_scoutage", ":cur_rents"),
			(val_mul, ":cur_scoutage", ":multiplier"),
			(val_div, ":cur_scoutage", 100),
			# Safety: scoutage is income; never allow it to go negative.
			(val_max, ":cur_scoutage", 0),
			(val_add, "$g_sod_weekly_scoutage", ":cur_scoutage"),
			# Safety: bound the accumulator.
			(val_clamp, "$g_sod_weekly_scoutage", 0, 2000001),
			(val_sub, ":cur_rents", ":cur_scoutage"), # FIX: ensure the player's scutage is actually taxed from the vassal's rents, rather than generating infinite wealth!
			# Safety: never allow negative rents after scoutage subtraction.
			(val_max, ":cur_rents", 0),
		(try_end),

        # debug
        (try_begin),
          (eq, "$g_sod_debug", 1),
          (str_store_party_name_link, s1, ":center_no"),
          (assign, reg0, ":cur_rents"),
          (display_message, "@The collectors from {s1} deliver {reg0} denars into your coffers this week.", debug_color),
        (try_end),

        # accumulate the rents & taxes
        (call_script, "script_sod_center_apply_rents_delta", ":center_no", ":cur_rents"),
    (try_end),
    ]
  ),
]
