SIMPLE_TRIGGERS = [
(24,
  [
    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 0),
    (try_end),

    # garrison applies to castles & towns (not villages)
    (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
		(store_faction_of_party, ":center_faction", ":center_no"),
        (try_begin), 
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
		
        # check if this center should stop garrisoning (is full)
			(party_get_slot, ":full", ":center_no", slot_center_max_garrison),
			(party_get_num_companions, ":garrison", ":center_no"),
			(lt, ":garrison", ":full"),
		
			(party_get_slot, ":soldiers", ":center_no", slot_center_garrison_soldiers),
			(party_get_slot, ":ranged", ":center_no", slot_center_garrison_ranged),
			(store_add, ":daily_garrisoning", ":soldiers", ":ranged"),
			(gt, ":daily_garrisoning", 0),

			# limit the garrison potential to the local population available (above the minimum required for that locale)
			(try_begin),
				# towns draw upon their own populations
				(party_slot_eq, ":center_no", slot_party_type, spt_town),
				(assign, ":population_center", ":center_no"),
				(party_get_slot, ":center_population", ":population_center", slot_center_sod_local_population),
				(store_sub, ":at_most", ":center_population", town_pop_min),
			(else_try),
				# castles must draw upon their associated village
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
				(assign, ":population_center", -1), # FIX: initialize to -1 to prevent draining wrong centers
				(try_for_range, ":village", villages_begin, villages_end),
					(party_slot_eq, ":village", slot_village_bound_center, ":center_no"),
					(assign, ":population_center", ":village"),
					(assign, ":village", villages_end), #break
				(try_end),
				(try_begin),
					(ge, ":population_center", 0),
					(party_get_slot, ":center_population", ":population_center", slot_center_sod_local_population),
					(store_sub, ":at_most", ":center_population", village_pop_min),
				(else_try),
					(assign, ":at_most", 0), # No bound village means no population to draw from
				(try_end),
			(try_end),
		
			(try_begin),
				(lt, ":at_most", ":daily_garrisoning"),
				(str_store_party_name_link, s2, ":center_no"),
				(display_message, "@Population in {s2} is too low to continue raising a garrison.", warning_color),
			(try_end),
		
			(ge, ":at_most", ":daily_garrisoning"),

			# keep track of how many we've actually garrisoned (so that we can remove them from the tax-paying population)
			(assign, ":garrisoned", 0),

			# ensure no error when we generate message text (much further down)
			(assign, ":soldier_id", 0),
			(assign, ":ranged_id", 0),

			# garrison foot party_add_members (if the player has asked the marshall to garrison foot party_add_members)
			(try_begin),
				(gt, ":soldiers", 0),

				# determine the correct troop type to garrison
				(try_begin),
					(eq, "$g_sod_country", cb_antares),
					(assign, ":soldier_id", "trp_sod_ant_regular"),
				(else_try),
					(eq, "$g_sod_country", cb_marina),
					(assign, ":soldier_id", "trp_sod_mar_conscript"),
				(else_try),
					(eq, "$g_sod_country", cb_aden),
					(assign, ":soldier_id", "trp_sod_ade_regular"),
				(else_try),
					(eq, "$g_sod_country", cb_villian),
					(assign, ":soldier_id", "trp_sod_vil_regular"),
				(else_try),
					(eq, "$g_sod_country", cb_zerrikan),
					(assign, ":soldier_id", "trp_sod_zer_1_infantry"),
				(try_end),

				# garrison the appropriate foot party_add_members
				(try_begin),
					(neq, ":soldier_id", 0),
					(party_add_members, ":center_no", ":soldier_id", ":soldiers"),
					#(try_for_range, ":unused", 0, ":soldiers"),
					#  (party_add_template, ":center_no", ":party_template"),
					#(try_end),
					(val_add, ":garrisoned", ":soldiers"),
				(try_end),
			(try_end),

			# check if we should be garrisoning ranged units
			(try_begin),
				(gt, ":ranged", 0),

				# determine the type of ranged units to garrison
				(try_begin),
					(eq, "$g_sod_country", cb_antares),
					(assign, ":ranged_id", "trp_sod_ant_javelinman"),
				(else_try),
					(eq, "$g_sod_country", cb_marina),
					(assign, ":ranged_id", "trp_sod_mar_crossbowman"),
				(else_try),
					(eq, "$g_sod_country", cb_aden),
					(assign, ":ranged_id", "trp_sod_ade_archer"),
				(else_try),
					(eq, "$g_sod_country", cb_villian),
					(assign, ":ranged_id", "trp_sod_vil_longbowman"),
				(else_try),
					(eq, "$g_sod_country", cb_zerrikan),
					(assign, ":ranged_id", "trp_sod_zer_1_archer"),
				(try_end),

				# garrison the appropriate ranged units
				(try_begin),
					(neq, ":ranged_id", 0),
					#(try_for_range, ":unused", 0, ":available"),
					#  (party_add_template, ":center_no", ":party_template"),
					#(try_end),
					(party_add_members, ":center_no", ":ranged_id", ":ranged"),
					(val_add, ":garrisoned", ":ranged"),
				(try_end),
			(try_end),

			(try_begin),
				(gt, ":garrisoned", 0),

				# remove the total population garrisoned from the local populace
				(val_sub, ":center_population", ":garrisoned"),
				(party_set_slot, ":population_center", slot_center_sod_local_population, ":center_population"),

				# inform the player, so they have a sense of how many and how fast garrison is proceeding
				(try_begin),
					(eq, "$g_sod_hide_messages", 0),

					# generate the text for what was actually garrisoned
					(assign, reg1, ":soldiers"),
					(store_sub, reg0, ":soldiers", 1),
					(str_store_troop_name_by_count, s1, ":soldier_id", ":soldiers"),
					(str_store_string, s2, "@{reg0?{reg1}:an} {s1}"),

					(assign, reg1, ":ranged"),
					(store_sub, reg0, ":ranged", 1),
					(str_store_troop_name_by_count, s1, ":ranged_id", ":ranged"),
					(str_store_string, s3, "@{reg0?{reg1}:an} {s1}"),

					(try_begin),
						(neq, ":soldiers", 0),
						(neq, ":ranged", 0),
						(str_store_string, s4, "@{s2} and {s3}"),
					(else_try),
						(neq, ":soldiers", 0),
						(str_store_string, s4, "@{s2}"),
					(else_try),
						(str_store_string, s4, "@{s3}"),
					(try_end),

					(str_store_party_name_link, s1, ":center_no"),
					(assign, reg1, ":garrisoned"),
					(try_begin),
						(party_slot_eq, ":center_no", slot_party_type, spt_castle),
						(str_store_party_name_link, s2, ":population_center"),
						(display_message, "@{s1} has raised {s4} for its garrison, drawing {reg1} villagers from {s2}.", pop_color),
					(else_try),
						(display_message, "@{s1} has raised {s4} for its garrison, drawing {reg1} citizens into service.", pop_color),
					(try_end),
				(try_end),
			(try_end),
		(try_end),
    (try_end),

    # attract lords (knights) from the old world (they don't deduct from the local populations) - compute the total from the kingdom
    (call_script, "script_update_nobles_gather_at"),

    # determine how many come (capped by population: high-tier nobles gated by realm size)
    (assign, ":nobles", 0),
    (assign, ":total_chapter_pop", 0),
    (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
		(store_faction_of_party, ":center_faction", ":center_no"),
		(eq, ":center_faction", "fac_player_supporters_faction"),
		(party_slot_eq, ":center_no", slot_center_has_chapter, 1),
		(try_begin),
		  (party_slot_eq, ":center_no", slot_party_type, spt_town),
		  (party_get_slot, ":pop", ":center_no", slot_center_sod_local_population),
		  (val_add, ":total_chapter_pop", ":pop"),
		(else_try),
		  (party_slot_eq, ":center_no", slot_party_type, spt_castle),
		  (try_for_range, ":village", villages_begin, villages_end),
		    (party_slot_eq, ":village", slot_village_bound_center, ":center_no"),
		    (party_get_slot, ":pop", ":village", slot_center_sod_local_population),
		    (val_add, ":total_chapter_pop", ":pop"),
		  (try_end),
		(try_end),
    (try_end),
    (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
		(store_faction_of_party, ":center_faction", ":center_no"),
		(eq, ":center_faction", "fac_player_supporters_faction"),
		(party_slot_eq, ":center_no", slot_center_has_chapter, 1),
		(store_add, ":happiness", "$g_sod_nobles_happines", 101),
		(store_div, ":pop_bonus", ":total_chapter_pop", sod_noble_happiness_pop_divisor),
		(val_min, ":pop_bonus", sod_noble_happiness_pop_bonus_max),
		(val_add, ":happiness", ":pop_bonus"),
		(ge, ":happiness", 50),
		(store_random_in_range, ":num", 0, ":happiness"),
		(store_div, ":num_nobles", ":num", 50),
		(val_add, ":nobles", ":num_nobles"),
    (try_end),

    (store_div, ":noble_cap", ":total_chapter_pop", sod_noble_cap_pop_divisor),
    (val_max, ":noble_cap", 1),
    (val_min, ":nobles", ":noble_cap"),

    (try_begin),
		(gt, ":nobles", 0),
		(try_begin),
			(eq, "$g_sod_country", cb_antares),
			(assign, ":nobles_id", "trp_sod_ant_noble"),
		(else_try),
			(eq, "$g_sod_country", cb_marina),
			(assign, ":nobles_id", "trp_sod_mar_mercenary"),
		(else_try),
			(eq, "$g_sod_country", cb_aden),
			(assign, ":nobles_id", "trp_sod_ade_sqire"),
		(else_try),
			(eq, "$g_sod_country", cb_villian),
			(assign, ":nobles_id", "trp_sod_vil_noble"),
		(else_try),
			#(party_slot_eq, "$g_sod_country", cb_zerrikan),
			(assign, ":nobles_id", "trp_sod_zer_1_noble"),
		(try_end),

		# generate the actual nobles
		(party_add_members, "$g_sod_nobles_gather_at", ":nobles_id", ":nobles"),
		(assign, ":nobles", reg0),

		# inform the player, so they have a sense of how many and how fast garrison is proceeding
		(try_begin),
			(eq, "$g_sod_hide_messages", 0),
			(call_script, "script_store_troop_name_link", s1, ":nobles_id"),
			(str_store_party_name_link, s2, "$g_sod_nobles_gather_at", faith_color),
			(assign, reg1, ":nobles"),
			(store_sub, reg0, ":nobles", 1),
			(str_store_string, s1, "@{reg0?{reg1}:An} {s1} came to {s2} from the Old World."),
			(display_message, s1, faith_color),
		(try_end),
    (try_end),
	
    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 1),
    (try_end),

  ]),
]
