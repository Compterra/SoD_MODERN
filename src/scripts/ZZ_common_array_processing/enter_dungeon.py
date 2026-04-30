SCRIPTS = [
("enter_dungeon",
    [
      (store_script_param_1, ":center_no"),
      (store_script_param_2, ":mission_template_no"),

      (set_jump_mission, ":mission_template_no"),
      (party_get_slot, ":dungeon_scene", ":center_no", slot_town_prison),

      (modify_visitors_at_site, ":dungeon_scene"), (reset_visitors),
      (assign, ":cur_pos", 16),
      (call_script, "script_get_heroes_attached_to_center_as_prisoner", ":center_no", "p_temp_party"),
      (party_get_num_companion_stacks, ":num_stacks", "p_temp_party"),
      (try_for_range, ":i_stack", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":i_stack"),
        (lt, ":cur_pos", 32), # spawn up to entry point 32
        (set_visitor, ":cur_pos", ":stack_troop"),
        (val_add, ":cur_pos", 1),
      (try_end),

      (set_jump_entry, 0),
      (jump_to_scene, ":dungeon_scene"),
      (scene_set_slot, ":dungeon_scene", slot_scene_visited, 1),
      (change_screen_mission),
  ]),
]
