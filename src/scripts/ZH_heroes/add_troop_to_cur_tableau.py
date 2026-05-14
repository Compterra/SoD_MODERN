SCRIPTS = [
("add_troop_to_cur_tableau",
      [
        (store_script_param, ":troop_no", 1),

        (set_fixed_point_multiplier, 100),
        (assign, ":banner_mesh", -1),
        (troop_get_slot, ":banner_spr", ":troop_no", slot_troop_banner_scene_prop),
        (store_add, ":banner_scene_props_end", banner_scene_props_end_minus_one, 1),
        (try_begin),
          (is_between, ":banner_spr", banner_scene_props_begin, ":banner_scene_props_end"),
          (val_sub, ":banner_spr", banner_scene_props_begin),
          (store_add, ":banner_mesh", ":banner_spr", banner_meshes_begin),
        (try_end),

        (cur_tableau_clear_override_items),

        #       (cur_tableau_set_override_flags, af_override_fullhelm),
        (cur_tableau_set_override_flags, af_override_head|af_override_weapons),

        (init_position, pos2),
        (cur_tableau_set_camera_parameters, 1, 6, 6, 10, 10000),

        (init_position, pos5),
        (assign, ":eye_height", 162),
        (store_mul, ":camera_distance", ":troop_no", 87323),
        #       (val_mod, ":camera_distance", 5),
        (assign, ":camera_distance", 139),
        (store_mul, ":camera_yaw", ":troop_no", 124337),
        (val_mod, ":camera_yaw", 50),
        (val_add, ":camera_yaw", -25),
        (store_mul, ":camera_pitch", ":troop_no", 98123),
        (val_mod, ":camera_pitch", 20),
        (val_add, ":camera_pitch", -14),
        (assign, ":animation", anim_stand_man),

        (position_set_z, pos5, ":eye_height"),

        # camera looks towards -z axis
        (position_rotate_x, pos5, -90),
        (position_rotate_z, pos5, 180),

        # now apply yaw and pitch
        (position_rotate_y, pos5, ":camera_yaw"),
        (position_rotate_x, pos5, ":camera_pitch"),
        (position_move_z, pos5, ":camera_distance", 0),
        (position_move_x, pos5, 5, 0),

        (try_begin),
          (ge, ":banner_mesh", 0),
		  (neg|is_between, ":troop_no", "trp_black_army_leader_1", "trp_kingdom_1_pretender"),

          (init_position, pos1),
          (position_set_z, pos1, -1500),
          (position_set_x, pos1, 265),
          (position_set_y, pos1, 400),
          (position_transform_position_to_parent, pos3, pos5, pos1),
          (cur_tableau_add_mesh, ":banner_mesh", pos3, 400, 0),
        (try_end),
        (cur_tableau_add_troop, ":troop_no", pos2, ":animation" , 0),

        (cur_tableau_set_camera_position, pos5),

        (copy_position, pos8, pos5),
        (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
        (position_rotate_z, pos8, 30),
        (position_rotate_x, pos8, -60),
        (cur_tableau_add_sun_light, pos8, 175, 150, 125),
    ]),
]
