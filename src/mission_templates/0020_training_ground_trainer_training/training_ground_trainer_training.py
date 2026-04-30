MISSION_TEMPLATES = [
(
    "training_ground_trainer_training", mtf_arena_fight, -1,
    "You will fight a match in the arena.",
    [
      (16, mtef_visitor_source|mtef_team_0, af_override_everything, aif_start_alarmed, 1, [itm_practice_shield, itm_practice_sword, itm_practice_boots]),
      (17, mtef_visitor_source|mtef_team_1, af_override_everything, aif_start_alarmed, 1, [itm_practice_staff, itm_practice_boots]),
      (18, mtef_visitor_source|mtef_team_2, af_override_everything, aif_start_alarmed, 1, [itm_practice_staff, itm_practice_boots]),
      (19, mtef_visitor_source|mtef_team_3, af_override_everything, aif_start_alarmed, 1, [itm_heavy_practice_sword, itm_practice_boots]),
      (20, mtef_visitor_source, 0, 0, 1, []),
    ],
    [
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      common_arena_fight_tab_press, 
	  common_battle_horse_health,

      (ti_question_answered, 0, 0, [],
       [
         (store_trigger_param_1, ":answer"),
         (eq, ":answer", 0),
         (set_jump_mission, "mt_training_ground_trainer_talk"),
         (modify_visitors_at_site, "$g_training_ground_melee_training_scene"),
         (reset_visitors),
         (set_jump_entry, 5),
         (jump_to_scene, "$g_training_ground_melee_training_scene"),
         ]),
      (1, 3, ti_once, [(main_hero_fallen, 0)],
       [
         (set_jump_mission, "mt_training_ground_trainer_talk"),
         (modify_visitors_at_site, "$g_training_ground_melee_training_scene"),
         (reset_visitors),
         (set_jump_entry, 5),
         (jump_to_scene, "$g_training_ground_melee_training_scene"),
         ]),
      (1, 3, ti_once,
       [
         (store_mission_timer_a, reg1),
         (ge, reg1, 1),
         (num_active_teams_le, 1),
         (neg|main_hero_fallen),
         (assign, "$training_fight_won", 1),
         ],
       [
         (set_jump_mission, "mt_training_ground_trainer_talk"),
         (modify_visitors_at_site, "$g_training_ground_melee_training_scene"),
         (reset_visitors),
         (set_jump_entry, 5),
         (jump_to_scene, "$g_training_ground_melee_training_scene"),
         ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message, "str_cant_use_inventory_arena", red)], []),
    ],
  ),
]
