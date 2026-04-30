MISSION_TEMPLATES = [
(
    "elephant_guard_training", mtf_team_fight, charge,
    "You will fight a match in the arena.",
    [
      (0, mtef_visitor_source|mtef_team_0, af_override_weapons, aif_start_alarmed, 1, [itm_practice_shield, itm_practice_sword]),
      (1, mtef_visitor_source|mtef_team_0, af_override_weapons, aif_start_alarmed, 1, [itm_practice_shield, itm_practice_sword]),
      (2, mtef_visitor_source|mtef_team_0, af_override_weapons, aif_start_alarmed, 1, [itm_practice_shield, itm_practice_sword]),
      (3, mtef_visitor_source|mtef_team_0, af_override_weapons, aif_start_alarmed, 1, [itm_practice_shield, itm_practice_sword]),
      (4, mtef_visitor_source|mtef_team_0, af_override_weapons, aif_start_alarmed, 1, [itm_practice_shield, itm_practice_sword]),
      (5, mtef_visitor_source|mtef_team_1, af_override_all, aif_start_alarmed, 1, [itm_practice_shield, itm_practice_sword, itm_leather_vest]),
	  (6, mtef_visitor_source|mtef_team_1, af_override_all, aif_start_alarmed, 1, [itm_practice_shield, itm_practice_sword, itm_leather_vest]),
      (7, mtef_visitor_source|mtef_team_1, af_override_all, aif_start_alarmed, 1, [itm_practice_shield, itm_practice_sword, itm_leather_vest]),
	  (8, mtef_visitor_source|mtef_team_1, af_override_all, aif_start_alarmed, 1, [itm_practice_shield, itm_practice_sword, itm_leather_vest]),
    ],
    [
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      common_arena_fight_tab_press, 

      (ti_question_answered, 0, 0, [],
       [
         (store_trigger_param_1, ":answer"),
         (eq, ":answer", 0),
         (set_jump_mission, "mt_mercenary_base"),
         (jump_to_scene, "$g_training_ground_melee_training_scene"),
         ]),
      (1, 3, ti_once, [(main_hero_fallen)],
       [
         (finish_mission),
         ]),
      (1, 3, ti_once,
       [
         (store_mission_timer_a, reg1),
         (ge, reg1, 1),
         (num_active_teams_le, 1),
         (neg|main_hero_fallen),
         ],
       [
		 (val_add, "$elephant_guard_training_groups_defeted", 1),
		 (try_begin),
			(eq, "$elephant_guard_training_groups_defeted", 1),
			(add_xp_as_reward, 200),
		 (else_try),
			(eq, "$elephant_guard_training_groups_defeted", 2),
			(add_xp_as_reward, 400),
		 (else_try),
			(eq, "$elephant_guard_training_groups_defeted", 3),
			(succeed_quest, "qst_elephant_guard_train_peasants_against_bandits"),
			(add_xp_as_reward, 600),
		 (try_end),
		 (finish_mission),
		 # (party_get_slot, ":base_scene", "$g_encountered_party", slot_castle_exterior),
		 # (store_faction_of_party, ":gm_fac", "$g_encountered_party"),
	     # (faction_get_slot, ":gm_troop", ":gm_fac", slot_guild_master),
		 # (assign, "$g_mt_mode", abm_visit),
		 # (set_jump_mission, "mt_mercenary_base"),
		 # (jump_to_scene,":base_scene"),
		 # (change_screen_map_conversation, ":gm_troop")
         ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message, "str_cant_use_inventory_arena", red)], []),
    ],
  ),
]
