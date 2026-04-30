SCRIPTS = [
("cf_turn_windmill_fans",
    [(store_script_param_1, ":instance_no"),
      (scene_prop_get_instance, ":windmill_fan_object", "spr_windmill_fan_turning", ":instance_no"),
      (ge, ":windmill_fan_object", 0),
      (prop_instance_get_position, pos1, ":windmill_fan_object"),
      (position_rotate_y, pos1, 10),
      (prop_instance_animate_to_position, ":windmill_fan_object", pos1, 100),
      (val_add, ":instance_no", 1),
      (call_script, "script_cf_turn_windmill_fans", ":instance_no"),
  ]),
]
