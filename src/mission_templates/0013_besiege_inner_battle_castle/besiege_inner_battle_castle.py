MISSION_TEMPLATES = [
(
    "besiege_inner_battle_castle", mtf_battle_mode, -1,
    "You attack the walls of the castle...",
    [
     (0, mtef_attackers|mtef_use_exact_number|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
     (6, mtef_attackers|mtef_use_exact_number|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
     (7, mtef_attackers|mtef_use_exact_number|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
     (16, mtef_defenders|mtef_use_exact_number|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
     (17, mtef_defenders|mtef_use_exact_number|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
     (18, mtef_defenders|mtef_use_exact_number|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
     (19, mtef_defenders|mtef_use_exact_number|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
     (20, mtef_defenders|mtef_use_exact_number|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
     ],
    [
      (ti_before_mission_start, 0, 0, [], [
        (call_script, "script_change_banners_and_chest"),
        (call_script, "script_sod_battle_initialize_morale_context"),
        (call_script, "script_sod_battle_xp_log_start"),
      ]),

      common_battle_tab_press, 
	  common_battle_horse_health, 
      common_battle_xp_log_suppression_tick,
      sod_battle_commander_spawn_player_ally_dismounted,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1, ":answer"),
        (eq, ":answer", 0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 5, 20),
        (assign, "$g_battle_result", -1),
        (set_mission_result, -1),
        (call_script, "script_sod_post_defeat_record_aftermath", -1),
        (call_script, "script_sod_post_defeat_count_casualties_once"),
        (call_script, "script_sod_post_defeat_clear"),
        (finish_mission, 0),
        ]),

      (0, 0, ti_once, [], [(assign, "$battle_won", 0),
                           (assign, "$g_presentation_battle_active", 0),
                           (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
                           ]),

      #AI Tiggers
      (0, 0, ti_once, [
          (assign, "$defender_team", 0),
          (assign, "$attacker_team", 1),
          (assign, "$defender_team_2", 2),
          (assign, "$attacker_team_2", 3),
          ], []),

      common_battle_check_friendly_kills,
      common_battle_check_victory_condition,
      common_battle_victory_display,

      (1, 4, ti_once, [(main_hero_fallen)],
          [
              (assign, "$pin_player_fallen", 1),
#SoD              (str_store_string, s5, "str_retreat"),
#SoD              (call_script, "script_simulate_retreat", 5, 20),
#SoD              (assign, "$g_battle_result", -1),
#SoD              (set_mission_result, -1),
#SoD              (call_script, "script_count_mission_casualties_from_agents"),
#SoD              (finish_mission, 0)
              ]),

      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_battle_inventory,

      camera_trigger_1,
      camera_trigger_2,
      camera_trigger_3,
      camera_trigger_4,
      camera_trigger_5,
      camera_trigger_6,
      camera_trigger_7,
      camera_trigger_8,

      formations_init_kill_count,
      formations_update_kill_count,
      formations_start_coherence,
    ],
  ),
]
