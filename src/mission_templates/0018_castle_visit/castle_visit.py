MISSION_TEMPLATES = [
(
    "castle_visit", 0, -1,
    "Castle visit",
    [(0, mtef_scene_source|mtef_team_0, af_override_horse, 0, 1, []),
     (1, mtef_scene_source|mtef_team_0, af_override_horse, 0, 1, []),
     (2, mtef_scene_source|mtef_team_0, af_override_horse, 0, 1, []),
     (3, mtef_scene_source|mtef_team_0, af_override_horse, 0, 1, []),
     (4, mtef_scene_source|mtef_team_0, af_override_horse, 0, 1, []),
     (5, mtef_scene_source|mtef_team_0, af_override_horse, 0, 1, []),
     (6, mtef_scene_source|mtef_team_0, af_override_horse, 0, 1, []),
     (7, mtef_scene_source|mtef_team_0, af_override_horse, 0, 1, []),
     (8, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (9, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (10, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (11, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     (12, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (13, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (14, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (15, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     (16, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (17, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (18, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (19, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     (20, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (21, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (22, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (23, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     (24, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (25, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (26, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (27, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     (28, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (29, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (30, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (31, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     (32, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (33, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (34, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (35, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     (36, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (37, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (38, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []), (39, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     # Party members
     (40, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     (41, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     (42, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     (43, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     (44, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     (45, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     (46, mtef_visitor_source|mtef_team_0, af_override_horse, 0, 1, []),
     ],
    [
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_init_town_agent", ":agent_no"),
         ]),
      (ti_tab_pressed, 0, 0, [(set_trigger_result, 1)], []),
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest"),
                                           (call_script, "script_remove_siege_objects"),
                                           ]),



#      (0, 0, ti_once, [], [(call_script, "script_music_set_situation_with_culture", mtf_sit_lords_hall), ]),

#      (ti_before_mission_start, 0, 0, [],
#          [(scene_prop_disable, "spr_ramp_12m"), (scene_prop_disable, "spr_portcullis")]),
    ],
  ),
]
