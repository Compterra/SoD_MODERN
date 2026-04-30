MISSION_TEMPLATES = [
(
    "village_training", mtf_arena_fight, -1,
    "village_training",
    [(2, mtef_visitor_source|mtef_team_0, af_override_everything, aif_start_alarmed, 1, [itm_practice_staff, itm_practice_boots]),
     (4, mtef_visitor_source|mtef_team_1, af_override_everything, aif_start_alarmed, 1, [itm_practice_staff, itm_practice_boots]),
     ],
    [
      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_train_peasants_against_bandits_training_succeeded", 0),
         (call_script, "script_change_banners_and_chest"),
         ]),

      common_arena_fight_tab_press, 
	  common_battle_horse_health,

      (ti_question_answered, 0, 0, [],
       [
         (store_trigger_param_1, ":answer"),
         (eq, ":answer", 0),
         (finish_mission),
         ]),

      common_inventory_not_available,

      (1, 4, ti_once,
       [
         (this_or_next|main_hero_fallen),
         (num_active_teams_le, 1)
         ],
       [
         (try_begin),
           (neg|main_hero_fallen),
           (assign, "$g_train_peasants_against_bandits_training_succeeded", 1),
         (try_end),
         (finish_mission),
         ]),
      ],
    ),
]
