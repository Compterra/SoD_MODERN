SIMPLE_TRIGGERS = [
(24,
  [
    (store_current_day, ":cur_day"),
    (store_sub, ":delta", "$g_sod_invasion_begin", ":cur_day"),
	(try_begin),
		(lt, ":delta", -5),	
		(eq, "$sod_credits_shown", 0),
		(neg|faction_slot_eq, "fac_kingdom_6", slot_faction_state, sfs_active),
		(map_free),
		(start_presentation, "prsnt_sod_credits"),
	(try_end),
    (ge, ":delta", 0),

    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 0),
    (try_end),
	
	#SoD - Kuba, start spawning dedicated Legion auxiliaries 3 months before the invasion.
	(try_begin),
		(eq, ":delta", 90),
		(faction_set_slot, "fac_kingdom_6_mercenaries", slot_faction_state, sfs_active),
		(try_for_range, ":cur_spawn_point", imperial_invasion_entry_villages_begin, imperial_invasion_entry_villages_end),
			(spawn_around_party, ":cur_spawn_point", "pt_legion_mercenaries"),
			(assign, ":merc_party", reg0),
			(gt, ":merc_party", 0),
			(party_is_active, ":merc_party"),
			(party_add_template, ":merc_party", "pt_legion_mercenaries"),
			(party_set_banner_icon, ":merc_party", "icon_banner_304"),
		(try_end),
	(else_try),
		(eq, ":delta", 60),
		(faction_set_slot, "fac_kingdom_6_mercenaries", slot_faction_state, sfs_active),
		(try_for_range, ":cur_spawn_point", imperial_invasion_entry_villages_begin, imperial_invasion_entry_villages_end),
			(spawn_around_party, ":cur_spawn_point", "pt_legion_mercenaries"),
			(assign, ":merc_party", reg0),
			(gt, ":merc_party", 0),
			(party_is_active, ":merc_party"),
			(party_add_template, ":merc_party", "pt_legion_mercenaries"),
			(party_add_template, ":merc_party", "pt_legion_mercenaries"),
			(party_set_banner_icon, ":merc_party", "icon_banner_304"),
		(try_end),
	(else_try),
		(eq, ":delta", 30),
		(faction_set_slot, "fac_kingdom_6_mercenaries", slot_faction_state, sfs_active),
		(try_for_range, ":cur_spawn_point", imperial_invasion_entry_villages_begin, imperial_invasion_entry_villages_end),
			(spawn_around_party, ":cur_spawn_point", "pt_legion_mercenaries"),
			(assign, ":merc_party", reg0),
			(gt, ":merc_party", 0),
			(party_is_active, ":merc_party"),
			(party_add_template, ":merc_party", "pt_legion_mercenaries"),
			(party_add_template, ":merc_party", "pt_legion_mercenaries"),
			(party_add_template, ":merc_party", "pt_legion_mercenaries"),
			(party_set_banner_icon, ":merc_party", "icon_banner_304"),
		(try_end),
	(try_end),
		
		
    #MORDACHAI: add a few warnings that the centurians have been spotted (30 days out, 15 days out, 7 days out, 1 day out)
    (try_begin),
      (is_between, ":delta", 16, 30),
      (display_message, "@Word spreads that the invaders are drawing closer.", warning_color),
    (else_try),
      (is_between, ":delta", 8, 16),
      (display_message, "@The invaders are said to be little more than a fortnight's march away.", warning_color),
    (else_try),
      (is_between, ":delta", 2, 8),
      (display_message, "@Scouts report the invaders just beyond the nearest hills!", red),
    (else_try),
      (eq, ":delta", 1),
      (display_message, "@The invaders are upon Calradia!", bright_red),
    (else_try),
      (eq, ":cur_day", "$g_sod_invasion_begin"),

      # activate the invaders faction
      (faction_set_slot, "fac_kingdom_6", slot_faction_state, sfs_active),

      # determine where the invasion will begin
      (store_random_in_range, ":village_no", imperial_invasion_entry_villages_begin, imperial_invasion_entry_villages_end),

      # create Legate Gaius Marius
      (troop_set_slot, "trp_kingdom_6_lord", slot_troop_wealth, 100000),
	  (troop_set_slot, "trp_kingdom_6_lord", slot_troop_occupation, slto_kingdom_hero),
      (troop_set_faction, "trp_kingdom_6_lord", "fac_kingdom_6"),
	  (call_script, "script_create_kingdom_hero_party", "trp_kingdom_6_lord", ":village_no"),
      (faction_set_slot, "fac_kingdom_6", slot_faction_central_center, ":village_no"), # SoD Twan : will help invaders find a good objective

      # activate the centurions
      (try_for_range, ":troop_no", "trp_knight_6_01", "trp_black_army_leader_1"),

        # only heros that aren't prisoners and who aren't yet leading a party...
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 1),

        # create a party for them & initial funds
        (troop_set_slot, ":troop_no", slot_troop_wealth, 40000),
        (call_script, "script_create_kingdom_hero_party", ":troop_no", ":village_no"),

      (try_end),   #twan453
	  
	  # generate war with everyone
      (set_show_messages, 0), # this is announced by a series of presentations - so redundant  #SoD Twan one menu to rule them all
      (call_script, "script_diplomacy_start_war_between_kingdoms", "fac_kingdom_6", "fac_kingdom_1", 3), # arg 3= no menu
      (call_script, "script_diplomacy_start_war_between_kingdoms", "fac_kingdom_6", "fac_kingdom_2", 3), 
      (call_script, "script_diplomacy_start_war_between_kingdoms", "fac_kingdom_6", "fac_kingdom_3", 3),
      (call_script, "script_diplomacy_start_war_between_kingdoms", "fac_kingdom_6", "fac_kingdom_4", 3),
      (call_script, "script_diplomacy_start_war_between_kingdoms", "fac_kingdom_6", "fac_kingdom_5", 3),
      (call_script, "script_diplomacy_start_war_between_kingdoms", "fac_kingdom_6", "fac_player_supporters_faction", 3),
      (set_show_messages, 1),

        (call_script, "script_sod_imperial_expedition_enforce_total_war"),
        (call_script, "script_set_faction_offensive_objective", "fac_kingdom_6"),
	    (call_script, "script_free_lords_estimate_their_situation"), #twan453
	  
     (str_store_party_name, s32, ":village_no"),
     (jump_to_menu, "mnu_invaders_arrived"),               # SoD Twan end
	  
    (try_end),

    (try_begin),
      (eq, "$g_sod_hide_messages", -2),
      (set_show_messages, 1),
    (try_end),
  ]
),
]
