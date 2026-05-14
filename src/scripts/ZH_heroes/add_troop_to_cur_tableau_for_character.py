SCRIPTS = [
("add_troop_to_cur_tableau_for_character",
      [
        (store_script_param, ":troop_no", 1),

        (set_fixed_point_multiplier, 100),

        (cur_tableau_clear_override_items),
        (cur_tableau_set_override_flags, af_override_fullhelm),

        (init_position, pos2),
        (cur_tableau_set_camera_parameters, 1, 4, 8, 10, 10000),

        (init_position, pos5),
        (assign, ":cam_height", 150),
        #       (val_mod, ":camera_distance", 5),
        (assign, ":camera_distance", 360),
        (assign, ":camera_yaw", -15),
        (assign, ":camera_pitch", -18),
        (assign, ":animation", anim_stand_man),

        (position_set_z, pos5, ":cam_height"),

        # camera looks towards -z axis
        (position_rotate_x, pos5, -90),
        (position_rotate_z, pos5, 180),

        # now apply yaw and pitch
        (position_rotate_y, pos5, ":camera_yaw"),
        (position_rotate_x, pos5, ":camera_pitch"),
        (position_move_z, pos5, ":camera_distance", 0),
        (position_move_x, pos5, 5, 0),

        (call_script, "script_sod_get_tableau_troop_seed", ":troop_no"),
        (cur_tableau_add_troop, ":troop_no", pos2, ":animation", reg0),
        (cur_tableau_set_camera_position, pos5),

        (copy_position, pos8, pos5),
        (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
        (position_rotate_z, pos8, 30),
        (position_rotate_x, pos8, -60),
        (cur_tableau_add_sun_light, pos8, 175, 150, 125),
    ]),
]
