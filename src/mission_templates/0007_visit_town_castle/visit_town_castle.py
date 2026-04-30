MISSION_TEMPLATES = [
(
    "visit_town_castle", 0, -1,
    "You enter the halls of the lord.",
    [(0, mtef_scene_source|mtef_team_0, af_override_horse|af_override_weapons|af_override_head, 0, 1, []),
     (1, mtef_scene_source|mtef_team_0, af_override_horse, 0, 1, []), (2, mtef_scene_source|mtef_team_0, af_override_horse, 0, 1, []), (3, mtef_scene_source|mtef_team_0, af_override_horse, 0, 1, []), (4, mtef_scene_source|mtef_team_0, af_override_horse, 0, 1, []), #for doors
     (5, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (6, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (7, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     (8, mtef_visitor_source, af_override_horse, 0, 1, []), (9, mtef_visitor_source, af_override_horse, 0, 1, []), (10, mtef_scene_source, af_override_horse, 0, 1, []), (11, mtef_scene_source, af_override_horse, 0, 1, []),
     (12, mtef_visitor_source, af_override_horse, 0, 1, []), (13, mtef_visitor_source, 0, 0, 1, []), (14, mtef_visitor_source, 0, 0, 1, []), (15, mtef_visitor_source, 0, 0, 1, []),
     (16, mtef_visitor_source, af_castle_lord, 0, 1, []), (17, mtef_visitor_source, af_castle_lord, 0, 1, []), (18, mtef_visitor_source, af_castle_lord, 0, 1, []), (19, mtef_visitor_source, af_castle_lord, 0, 1, []), (20, mtef_visitor_source, af_castle_lord, 0, 1, []), (21, mtef_visitor_source, af_castle_lord, 0, 1, []), (22, mtef_visitor_source, af_castle_lord, 0, 1, []), (23, mtef_visitor_source, af_castle_lord, 0, 1, []), (24, mtef_visitor_source, af_castle_lord, 0, 1, []),
     (25, mtef_visitor_source, af_castle_lord, 0, 1, []), (26, mtef_visitor_source, af_castle_lord, 0, 1, []), (27, mtef_visitor_source, af_castle_lord, 0, 1, []), (28, mtef_visitor_source, af_castle_lord, 0, 1, []), (29, mtef_visitor_source, af_castle_lord, 0, 1, []), (30, mtef_visitor_source, af_castle_lord, 0, 1, []), (31, mtef_visitor_source, af_castle_lord, 0, 1, [])
     ],
    [
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_init_town_agent", ":agent_no"),
         ]),
      (ti_before_mission_start, 0, 0, [],
       [
         (call_script, "script_change_banners_and_chest"),
         ]),
      (ti_inventory_key_pressed, 0, 0, [(set_trigger_result, 1)], []),
      (ti_tab_pressed, 0, 0, [(set_trigger_result, 1)], []),
      (0, 0, ti_once, [], [
        #(set_fog_distance, 150, 0xFF736252)
        (try_begin),
          (eq, "$talk_context", tc_court_talk),
#          (call_script, "script_music_set_situation_with_culture", mtf_sit_lords_hall),
        (else_try),
          (call_script, "script_music_set_situation_with_culture", 0), #prison
        (try_end),
        ]),
    ],
  ),
]
