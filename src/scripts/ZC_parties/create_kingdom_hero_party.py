SCRIPTS = [
("create_kingdom_hero_party",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":center_no", 2),

      (store_troop_faction, ":troop_faction_no", ":troop_no"),

      (assign, "$pout_party", -1),
      (set_spawn_radius, 0),
      (spawn_around_party, ":center_no", "pt_kingdom_hero_party"),
      (assign, "$pout_party", reg0),

      (party_set_faction, "$pout_party", ":troop_faction_no"),
      (party_set_slot, "$pout_party", slot_party_type, spt_kingdom_hero_party),
      (call_script, "script_party_set_ai_state", "$pout_party", spai_undefined, -1),
      (troop_set_slot, ":troop_no", slot_troop_leaded_party, "$pout_party"),
      (party_add_leader, "$pout_party", ":troop_no"),
	  (call_script, "script_store_troop_name_fief", s5, ":troop_no"),
      (party_set_name, "$pout_party", s5),

      (party_set_slot, "$pout_party", slot_party_commander_party, -1), #we need this because 0 is player's party!

      #Setting the flag icon
      #normal_banner_begin
	  (try_begin),
			(troop_get_slot, ":cur_banner", ":troop_no", slot_troop_banner_scene_prop),
			(gt, ":cur_banner", 0),
			(val_sub, ":cur_banner", banner_scene_props_begin),
			(val_add, ":cur_banner", banner_map_icons_begin),
			(party_set_banner_icon, "$pout_party", ":cur_banner"),
        # custom_banner_begin
		#		(troop_get_slot, ":flag_icon", ":troop_no", slot_troop_custom_banner_map_flag_type),
        #        (ge, ":flag_icon", 0),
        #        (val_add, ":flag_icon", custom_banner_map_icons_begin),
        #        (party_set_banner_icon, "$pout_party", ":flag_icon"),
      (try_end),

      (try_begin),
        (troop_slot_eq, ":troop_no", slot_troop_spawned_before, 0),
        (troop_set_slot, ":troop_no", slot_troop_spawned_before, 1),
        (assign, ":num_tries", 20),
	  (else_try),
        (assign, ":num_tries", 3),
      (try_end),		
		
        (try_begin),
          (store_troop_faction, ":troop_kingdom", ":troop_no"),
          (faction_slot_eq, ":troop_kingdom", slot_faction_leader, ":troop_no"),
          (assign, ":num_tries", 50),
        (try_end),

        (try_for_range, ":unused", 0, ":num_tries"),
          (call_script, "script_hire_men_to_kingdom_hero_party", ":troop_no"),
        (try_end),

        (store_random_in_range, ":xp_rounds", 2, 6),
        (troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
        (store_div, ":renown_xp_rounds", ":renown", 100),
        (val_add, ":xp_rounds", ":renown_xp_rounds"),

        (try_for_range, ":unused", 0, ":xp_rounds"),
          (call_script, "script_cf_party_upgrade_with_xp", "$pout_party", 4000),
        (try_end),

        # Troops come from pops: deduct spawn center population when lord party is created
        (party_get_num_companions, ":troops_created", "$pout_party"),
        (val_sub, ":troops_created", 1),
        (try_begin),
        (gt, ":troops_created", 0),
        (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (party_get_slot, ":pop", ":center_no", slot_center_sod_local_population),
        (val_sub, ":pop", ":troops_created"),
        (val_max, ":pop", town_pop_min),
        (party_set_slot, ":center_no", slot_center_sod_local_population, ":pop"),
        (else_try),
        (is_between, ":center_no", villages_begin, villages_end),
        (party_get_slot, ":pop", ":center_no", slot_center_sod_local_population),
        (val_sub, ":pop", ":troops_created"),
        (val_max, ":pop", village_pop_min),
        (party_set_slot, ":center_no", slot_center_sod_local_population, ":pop"),
        (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (try_for_range, ":village", villages_begin, villages_end),
        (party_slot_eq, ":village", slot_village_bound_center, ":center_no"),
        (party_get_slot, ":pop", ":village", slot_center_sod_local_population),
        (val_sub, ":pop", ":troops_created"),
        (val_max, ":pop", village_pop_min),
        (party_set_slot, ":village", slot_center_sod_local_population, ":pop"),
        (assign, ":village", villages_end),
        (try_end),
        (try_end),
        (try_end),
  ]),
]
