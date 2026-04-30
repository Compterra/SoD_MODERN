PRESENTATIONS = [
("sod_law", 0, 0,
   [
     (ti_on_presentation_load,
      [
		(call_script, "script_sod_law_migrate_player_legacy_slots"),
		(call_script, "script_clear_law_presentation_obj"),
		(set_fixed_point_multiplier, 1000),
# ###################################################################################################
# ###################################################################################################
		#DISPLAY BACGROUND
		(store_add, ":cur_page_mesh", "$law_cur_page", law_backgrounds_begin),
		(create_mesh_overlay, reg1, ":cur_page_mesh"),

        (position_set_x, pos1, 0),
        (position_set_y, pos1, 0),
        (overlay_set_position, reg1, pos1),
# ###################################################################################################
# ###################################################################################################		
		#GET ACTIVE LAW NAME & DESCRIPTION
		(store_add, ":pres_sod_active_law_name", "$law_cur_law", law_names_begin),
		(store_add, ":pres_sod_active_law_description", "$law_cur_law", law_descriptions_begin),
		(str_store_string, s1, ":pres_sod_active_law_name"),
		(str_store_string, s2, ":pres_sod_active_law_description"),
# ###################################################################################################
# ###################################################################################################			
		#DISPLAY ACTIVE LAW NAME
		(create_text_overlay, reg1, "@{s1}", tf_center_justify),
        (position_set_x, pos1, 155),
        (position_set_y, pos1, 410),
        (overlay_set_position, reg1, pos1),
		(position_set_x, pos1, 1200),
        (position_set_y, pos1, 1200),
        (overlay_set_size, reg1, pos1),
# ###################################################################################################
# ###################################################################################################		
		#DISPLAY ACTIVE LAW DESCRIPTION
		(create_text_overlay, reg1, "@{s2}", tf_center_justify|tf_double_space|tf_scrollable),
        (position_set_x, pos1, 50),
        (position_set_y, pos1, 50),
        (overlay_set_position, reg1, pos1),
		(position_set_x, pos1, 190),
        (position_set_y, pos1, 350),
        (overlay_set_area_size, reg1, pos1),
		(position_set_x, pos1, 900),
        (position_set_y, pos1, 900),
        (overlay_set_size, reg1, pos1),
# ###################################################################################################
# ###################################################################################################		
		#DISPLAY LARGE ACTIVE LAW PIC
		(store_add, ":pres_sod_active_law_mesh", "$law_cur_law", law_meshes_begin),
		(create_image_button_overlay, reg1, ":pres_sod_active_law_mesh", ":pres_sod_active_law_mesh"),
        (position_set_x, pos1, 48),
        (position_set_y, pos1, 489),
        (overlay_set_position, reg1, pos1),
		
		(position_set_x, pos1, 210),
        (position_set_y, pos1, 279),
        (overlay_set_size, reg1, pos1),
		
# ###################################################################################################
# ###################################################################################################
		(store_add, "$law_buttons_begin", reg1, 1),
		#DISPLAY 9 LAWS
		(store_mul, ":cur_page_laws_begin", "$law_cur_page", 10),
		(val_add, ":cur_page_laws_begin", 1),
		(store_add, ":cur_page_laws_end", ":cur_page_laws_begin", 9),
		
		(assign, ":x", 468),
		(assign, ":y", 50),
		
		(assign, ":count", 0),
		(try_for_range, ":cur_law", ":cur_page_laws_begin", ":cur_page_laws_end"),
			(store_add, ":cur_law_mesh", ":cur_law", law_meshes_begin),
			(create_image_button_overlay, reg1, ":cur_law_mesh", ":cur_law_mesh"),
		
			(position_set_x, pos1, ":x"),
			(position_set_y, pos1, ":y"),
			(overlay_set_position, reg1, pos1),
				
			(position_set_x, pos1, 105),
			(position_set_y, pos1, 141),
			(overlay_set_size, reg1, pos1),
			
			(val_add, ":count", 1),
			(try_begin),
				(this_or_next|eq, ":count", 3),
				(eq, ":count", 6),
				(assign, ":y", 50),
				(val_add, ":x", 130),
			(else_try),
				(val_add, ":y", 130),
			(try_end),
		(try_end),
# ###################################################################################################
# ###################################################################################################
		(store_add, "$enacted_law_buttons_begin", "$law_buttons_begin", 9),
		#DISPLAY 10 ENACTED LAWS
		(assign, ":x", 338),
		(assign, ":y", 604),
		
		(assign, ":count", 0),
		(try_for_range, ":cur_law_pointer", faction_laws_begin, faction_laws_end),
			(faction_get_slot, ":cur_law", "fac_player_supporters_faction", ":cur_law_pointer"),
			(store_add, ":cur_law_mesh", ":cur_law", law_meshes_begin),
			(create_image_button_overlay, reg1, ":cur_law_mesh", ":cur_law_mesh"),
		
			(position_set_x, pos1, ":x"),
			(position_set_y, pos1, ":y"),
			(overlay_set_position, reg1, pos1),
				
			(position_set_x, pos1, 105),
			(position_set_y, pos1, 141),
			(overlay_set_size, reg1, pos1),
			
			(val_add, ":count", 1),
			(try_begin),
				(eq, ":count", 5),
				(assign, ":y", 474),
				(assign, ":x", 338),
			(else_try),
				(val_add, ":x", 130),
			(try_end),
		(try_end),
# ###################################################################################################
# ###################################################################################################
		#DISPLAY NEXT PAGE AND PREVIOUS PAGE BUTTONS
		(create_game_button_overlay, "$pres_law_nextpage", "@Next", tf_center_justify),
        (position_set_x, pos1, 924),
        (position_set_y, pos1, 180),
        (overlay_set_position, "$pres_law_nextpage", pos1),
		(position_set_x, pos1, 130),
        (position_set_y, pos1, 40),
        (overlay_set_size, "$pres_law_nextpage", pos1),
		(create_game_button_overlay, "$pres_law_prevpage", "@Back", tf_center_justify),
        (position_set_x, pos1, 924),
        (position_set_y, pos1, 240),
        (overlay_set_position, "$pres_law_prevpage", pos1),
		(position_set_x, pos1, 130),
        (position_set_y, pos1, 40),
        (overlay_set_size, "$pres_law_prevpage", pos1),
# ###################################################################################################
# ###################################################################################################
		#DISPLAY DISMISS LAW BUTTONS    
		(try_begin),		
			(neq, "$law_cur_law", 0),
			(call_script, "script_sod_law_can_dismiss_for_faction", "fac_player_supporters_faction", "$law_cur_law"),
			(eq, reg0, 1),
			(create_game_button_overlay, "$pres_law_dismiss", "@Dismiss", tf_center_justify),
			(position_set_x, pos1, 924),
			(position_set_y, pos1, 310),
			(overlay_set_position, "$pres_law_dismiss", pos1),
			(position_set_x, pos1, 130),
			(position_set_y, pos1, 40),
			(overlay_set_size, "$pres_law_dismiss", pos1),
		(try_end),
# ###################################################################################################
# ###################################################################################################
#DISPLAY ENACT LAW BUTTON		
		(try_begin),		
			(neq, "$law_cur_law", 0),
			(call_script, "script_sod_law_can_enact_for_faction", "fac_player_supporters_faction", "$law_cur_law"),
			(eq, reg0, 1),

			(create_game_button_overlay, "$pres_law_enact", "@Enact", tf_center_justify),
			
			(position_set_x, pos1, 924),
			(position_set_y, pos1, 370),
			(overlay_set_position, "$pres_law_enact", pos1),
			(position_set_x, pos1, 130),
			(position_set_y, pos1, 40),
			(overlay_set_size, "$pres_law_enact", pos1),
		(try_end),
# ###################################################################################################
# ###################################################################################################
		#DISPLAY WHY A SELECTED LAW CANNOT BE ENACTED
		(try_begin),
			(neq, "$law_cur_law", 0),
			(call_script, "script_sod_law_can_enact_for_faction", "fac_player_supporters_faction", "$law_cur_law"),
			(eq, reg0, 0),
			(assign, ":block_reason", reg1),
			(assign, ":related_law", reg2),
			(call_script, "script_sod_law_store_block_reason_text", ":block_reason", ":related_law"),
			(create_text_overlay, reg1, "@{s13}", tf_center_justify),
			(position_set_x, pos1, 835),
			(position_set_y, pos1, 420),
			(overlay_set_position, reg1, pos1),
			(position_set_x, pos1, 500),
			(position_set_y, pos1, 650),
			(overlay_set_size, reg1, pos1),
		(try_end),
# ###################################################################################################
# ###################################################################################################			
		#DISPLAY LEAVE BUTTON
		(create_game_button_overlay, "$pres_law_leave", "@Leave", tf_center_justify),
        (position_set_x, pos1, 924),
        (position_set_y, pos1, 40),
        (overlay_set_position, "$pres_law_leave", pos1),
		(position_set_x, pos1, 130),
        (position_set_y, pos1, 40),
        (overlay_set_size, "$pres_law_leave", pos1),
		
        (presentation_set_duration, 999999),
        ]),
# ###################################################################################################
# ###################################################################################################			
     (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
# ###################################################################################################
# ###################################################################################################	
	    (try_begin),
			(eq, ":object", "$pres_law_enact"),
			(call_script, "script_sod_law_add_to_faction", "fac_player_supporters_faction", "$law_cur_law"),
			(assign, "$law_cur_law", 0),
		    (start_presentation, "prsnt_sod_law"),
# ###################################################################################################
# ###################################################################################################	
		(else_try),
			(eq, ":object", "$pres_law_dismiss"),
			(call_script, "script_sod_law_remove_from_faction", "fac_player_supporters_faction", "$law_cur_law"),
			(assign, "$law_cur_law", 0),
			(start_presentation, "prsnt_sod_law"),
# ###################################################################################################
# ###################################################################################################	
		(else_try),
			(eq, ":object", "$pres_law_leave"),
		    (presentation_set_duration, 0),
# ###################################################################################################
# ###################################################################################################	
		(else_try),
			(eq, ":object", "$pres_law_nextpage"),
			(try_begin),
				(eq, "$law_cur_page", 3),
				(assign, "$law_cur_page", 0),
			(else_try),
				(val_add, "$law_cur_page", 1),
			(try_end),
			(start_presentation, "prsnt_sod_law"),
# ###################################################################################################
# ###################################################################################################	
		(else_try),
			(eq, ":object", "$pres_law_prevpage"),
			(try_begin),
				(eq, "$law_cur_page", 0),
				(assign, "$law_cur_page", 3),
			(else_try),
				(val_sub, "$law_cur_page", 1),
			(try_end),
			(start_presentation, "prsnt_sod_law"),
# ###################################################################################################
# ###################################################################################################	
		(else_try),
		    (is_between, ":object", "$law_buttons_begin", "$enacted_law_buttons_begin"),
			(store_sub, ":new_law", ":object", "$law_buttons_begin"),
			(val_add, ":new_law", 1),
			(store_mul, ":page_step", "$law_cur_page", 10),
			(val_add, ":new_law", ":page_step"),
			
			(assign, "$law_cur_law", ":new_law"),
		    (start_presentation, "prsnt_sod_law"),
# ###################################################################################################
# ###################################################################################################	
		(else_try),
		    (is_between, ":object", "$enacted_law_buttons_begin", "$pres_law_nextpage"),
			(store_sub, ":new_law_pointer", ":object", "$enacted_law_buttons_begin"),
			(val_add, ":new_law_pointer", faction_laws_begin),
			(faction_get_slot, ":new_law", "fac_player_supporters_faction", ":new_law_pointer"),
			
			(assign, "$law_cur_law", ":new_law"),
		    (start_presentation, "prsnt_sod_law"),
# ###################################################################################################
# ###################################################################################################	
		(try_end),
        ]),
     ]),
]
