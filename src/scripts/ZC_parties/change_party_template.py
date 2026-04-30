SCRIPTS = [
("change_party_template", [
		(store_script_param_1, ":party_no"),
		(store_script_param_2, ":template_no"),
		
		(party_get_template_id, ":cur_template", ":party_no"),
		(try_begin),
			(neq, ":cur_template", ":template_no"),
			(str_store_party_name, s19, ":party_no"), # copy it's name
			(set_spawn_radius, 0),
			(spawn_around_party, ":party_no", ":template_no"),
			(assign, ":new_party", reg0),
			(party_set_name, ":new_party", s19),
			(assign, "$g_move_heroes", 1), #twan new
			(call_script, "script_party_add_party", ":new_party", ":party_no"),
			(assign, "$g_move_heroes", 0), #twan new
			(try_for_range, ":cur_slot", 0, 500), # copy all slots
				(party_get_slot, ":cur_value", ":party_no", ":cur_slot"),
				(party_set_slot, ":new_party", ":cur_slot", ":cur_value"),
			(try_end),
			(assign, ":party_leader", 0),
			(try_for_range, ":troop_no", kingdom_heroes_begin, kingdom_heroes_end),
				(troop_slot_eq, ":troop_no", slot_troop_leaded_party, ":party_no"),
				(troop_set_slot, ":troop_no", slot_troop_leaded_party, ":new_party"),
				(assign, ":party_leader", ":troop_no"),
			(try_end),
			(store_faction_of_party, ":cur_faction", ":party_no"), #copy it's faction
			(party_set_faction, ":new_party", ":cur_faction"),
			(try_begin), # set banner icon for the party with new template
				(gt, ":party_leader", 0),
				(troop_get_slot, ":cur_banner", ":party_leader", slot_troop_banner_scene_prop),
				(val_sub, ":cur_banner", banner_scene_props_begin),
				(val_add, ":cur_banner", banner_map_icons_begin),
				(party_set_banner_icon, ":new_party", ":cur_banner"),
			(else_try),
				(eq, "$g_custom_banner", 0),
				(troop_get_slot, ":cur_banner", "trp_player", slot_troop_banner_scene_prop),
				(val_sub, ":cur_banner", banner_scene_props_begin),
				(val_add, ":cur_banner", banner_map_icons_begin),
				(party_set_banner_icon, ":new_party", ":cur_banner"),
			(else_try),
				(troop_get_slot, ":flag_icon", "trp_player", slot_troop_custom_banner_map_flag_type),
				(val_max, ":flag_icon", 0),
				(val_add, ":flag_icon", custom_banner_map_icons_begin),
				(party_set_banner_icon, ":new_party", ":flag_icon"),
			(try_end), # copy ai behavior
			
			(try_for_parties, ":other_party"),         # Twan new : make so followers like mercs don't lose their commander party
			(party_slot_eq, ":other_party", slot_party_commander_party, ":party_no"),
			(party_set_slot, ":other_party", slot_party_commander_party, ":new_party"),
			(try_end),                                 # twan new end
			
			(get_party_ai_behavior, ":cur_bhvr", ":party_no"),
			(get_party_ai_object, ":cur_ai_obj", ":party_no"),
			(party_get_ai_target_position, pos1, ":party_no"),
			(party_set_ai_behavior, ":new_party", ":cur_bhvr"),
			(party_set_ai_object, ":new_party", ":cur_ai_obj"),
			(party_set_ai_target_position, ":new_party", pos1),
			(remove_party, ":party_no"),
			(assign, "$g_encountered_party", ":new_party"),
			(call_script, "script_process_hero_ai", ":party_leader"), # may help to avoid waiting parties
		(try_end),
		]),
]
