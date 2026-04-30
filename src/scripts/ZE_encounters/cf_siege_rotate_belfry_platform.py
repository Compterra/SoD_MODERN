SCRIPTS = [
("cf_siege_rotate_belfry_platform",
      [(eq, "$belfry_positioned", 1),
        (scene_prop_get_instance, ":belfry_object", "spr_belfry_platform_a", 0),
        (prop_instance_get_position, pos1, ":belfry_object"),
        (position_rotate_x, pos1, -90),
        (prop_instance_animate_to_position, ":belfry_object", pos1, 400),
        (assign, "$belfry_positioned", 2),
    ]),
]
