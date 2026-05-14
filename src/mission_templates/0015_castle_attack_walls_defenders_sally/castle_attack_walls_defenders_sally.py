MISSION_TEMPLATES = [
(
    "castle_attack_walls_defenders_sally", mtf_battle_mode, -1,
    "You attack the walls of the castle...",
    [
     (0, mtef_attackers|mtef_team_1, af_override_horse, aif_start_alarmed, 12, []),
     (0, mtef_attackers|mtef_team_1, af_override_horse, aif_start_alarmed, 0, []),
     (3, mtef_defenders|mtef_team_0, af_override_horse, aif_start_alarmed, 12, []),
     (3, mtef_defenders|mtef_team_0, af_override_horse, aif_start_alarmed, 0, []),
     ],
    [
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_agent_reassign_team", ":agent_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (team_set_relation, 0, 2, 1),
         (team_set_relation, 1, 3, 1),
         (call_script, "script_change_banners_and_chest"),
         (call_script, "script_sod_battle_initialize_morale_context"),
         (call_script, "script_remove_siege_objects"),
         ]),

      common_battle_tab_press, 
	  common_battle_horse_health, 
      sod_battle_commander_spawn_player_ally_dismounted,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1, ":answer"),
        (eq, ":answer", 0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 5, 20),
        (call_script, "script_sod_post_defeat_record_aftermath", -1),
        (call_script, "script_sod_post_defeat_count_casualties_once"),
        (call_script, "script_sod_post_defeat_clear"),
        (finish_mission, 0), ]),

      (0, 0, ti_once, [], [(assign, "$battle_won", 0),
                           (assign, "$g_presentation_battle_active", 0),
                           (call_script, "script_combat_music_set_situation_with_culture"),
                           ]),

      common_music_situation_update,
      common_battle_check_friendly_kills,

      (1, 60, ti_once, [(store_mission_timer_a, reg(1)),
                        (ge, reg(1), 10),
                        (all_enemies_defeated, 2),
                #SoD        (neg|main_hero_fallen, 0),
                        (set_mission_result, 1),
                        (display_message, "str_msg_battle_won", bright_green),
                        (assign, "$battle_won", 1),
                        (assign, "$g_battle_result", 1),
                        (assign, "$g_siege_sallied_out_once", 1),
                        (assign, "$g_siege_method", 1), #reset siege timer
                        (call_script, "script_play_victorious_sound"),
                        ],
           [(call_script, "script_sod_post_defeat_record_aftermath", 1),
            (call_script, "script_sod_post_defeat_count_casualties_once"),
            (call_script, "script_sod_post_defeat_clear"),
            (finish_mission, 1)]),

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
      formations_update_morale,
      formations_update_route,
    ],
  ),
]
