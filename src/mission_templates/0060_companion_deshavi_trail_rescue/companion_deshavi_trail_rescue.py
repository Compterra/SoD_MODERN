MISSION_TEMPLATES = [
(
    "companion_deshavi_trail_rescue", mtf_battle_mode, charge,
    "Deshavi's trail rescue",
    [
      (0, mtef_visitor_source|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
      (1, mtef_visitor_source|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
      (2, mtef_visitor_source|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
      (3, mtef_visitor_source|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
      (10, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
      (11, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
      (12, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
      (13, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
    ],
    [
      common_inventory_not_available,

      (ti_tab_pressed, 0, 0, [(display_message, "@Cannot leave now.", red)], []),

      (ti_before_mission_start, 0, 0, [],
       [
         (call_script, "script_change_banners_and_chest"),
       ]),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_fight),
         (set_party_battle_mode),
       ]),

      (1, 4, ti_once,
       [
         (store_mission_timer_a, ":cur_time"),
         (ge, ":cur_time", 3),
         (this_or_next|main_hero_fallen),
         (num_active_teams_le, 1),
       ],
       [
         (try_begin),
           (main_hero_fallen),
           (assign, "$g_sod_deshavi_trail_result_grade", -1),
           (jump_to_menu, "mnu_deshavi_tracks_rescue_failed"),
         (else_try),
           (try_begin),
             (call_script, "script_cf_troop_agent_is_alive", "trp_npc7"),
             (assign, "$g_sod_deshavi_trail_result_grade", 3),
           (else_try),
             (assign, "$g_sod_deshavi_trail_result_grade", 2),
           (try_end),
           (jump_to_menu, "mnu_deshavi_tracks_rescue_succeeded"),
         (try_end),
         (finish_mission),
       ]),

      formations_init_kill_count,
      formations_update_kill_count,
    ],
  ),
]
