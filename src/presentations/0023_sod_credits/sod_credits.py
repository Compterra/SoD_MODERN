PRESENTATIONS = [
("sod_credits", prsntf_read_only, 0,[
	  (ti_on_presentation_load, [
			(set_fixed_point_multiplier, 1000),
			(presentation_set_duration, 99999),
			(create_mesh_overlay, reg1, "mesh_sod_credits"),
			(position_set_x, pos1, 0),
			(position_set_y, pos1, 0),
			(overlay_set_position, reg1, pos1),
	  ]),
	  
	  (ti_on_presentation_run,
       [
        (try_begin),
            (this_or_next|key_clicked, key_escape),
			(this_or_next|game_key_clicked, gk_jump),
			(this_or_next|game_key_clicked, gk_attack),
			(game_key_clicked, gk_defend),
			(start_presentation, "prsnt_sod_description"),
        (try_end),
        ]),
	]),
]
