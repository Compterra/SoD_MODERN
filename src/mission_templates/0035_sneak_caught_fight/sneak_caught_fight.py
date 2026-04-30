MISSION_TEMPLATES = [
(
    "sneak_caught_fight", mtf_arena_fight, -1,
    "You must fight your way out!",
    [
      (0, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, pilgrim_disguise),
      (25, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
      (26, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
      (27, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
      (28, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
      (29, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
      (30, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
      (31, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
      (32, mtef_visitor_source|mtef_team_1, af_override_horse, aif_start_alarmed, 1, []),
#      (9, mtef_visitor_source|mtef_team_0, 0, aif_start_alarmed, 1, []),
    ],
    [
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),
      (ti_tab_pressed, 0, 0, [],
       [(question_box, "str_do_you_wish_to_surrender")]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1, ":answer"), (eq, ":answer", 0), (jump_to_menu, "mnu_captivity_start_castle_defeat"), (finish_mission, 0), ]),

      (1, 0, ti_once, [],
       [
         (play_sound, "snd_sneak_town_halt"),
         (call_script, "script_music_set_situation_with_culture", mtf_sit_fight),
         ]),
      (0, 3, 0,
       [
           (main_hero_fallen, 0),
        ],
       [(jump_to_menu, "mnu_captivity_start_castle_defeat"), (finish_mission, 0)]),
      (5, 1, ti_once, [(num_active_teams_le, 1), (neg|main_hero_fallen)],
       [(assign, "$auto_menu", -1), (jump_to_menu, "mnu_sneak_into_town_caught_dispersed_guards"), (finish_mission, 1)]),
      (ti_on_leave_area, 0, ti_once, [],
       [(assign, "$auto_menu", -1), (jump_to_menu, "mnu_sneak_into_town_caught_ran_away"), (finish_mission, 0)]),

      (ti_inventory_key_pressed, 0, 0, [(display_message, "str_cant_use_inventory_arena", red), red], []),

      formations_init_kill_count,
      formations_update_kill_count,
    ],
  ),
]
