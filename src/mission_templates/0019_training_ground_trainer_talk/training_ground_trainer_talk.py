MISSION_TEMPLATES = [
(
    "training_ground_trainer_talk", 0, -1,
    "Training.",
    [
      (0, mtef_scene_source|mtef_team_0, af_override_horse|af_override_weapons, 0, 1, []),
      (1, mtef_scene_source|mtef_team_0, af_override_horse|af_override_weapons, 0, 1, []),
      (2, mtef_scene_source|mtef_team_0, af_override_horse|af_override_weapons, 0, 1, []),
      (3, mtef_scene_source|mtef_team_0, af_override_horse|af_override_weapons, 0, 1, []),
      (4, mtef_scene_source|mtef_team_0, af_override_horse|af_override_weapons, 0, 1, []),
      (5, mtef_scene_source|mtef_team_0, af_override_horse|af_override_weapons, 0, 1, []),
      (6, mtef_scene_source|mtef_team_0, 0, 0, 1, []),
    ],
    [
      (ti_before_mission_start, 0, 0, [],
       [
         (call_script, "script_change_banners_and_chest"),
         ]),
      (ti_inventory_key_pressed, 0, 0,
       [
         (set_trigger_result, 1),
         ], []),
      (ti_tab_pressed, 0, 0,
       [
         (set_trigger_result, 1),
         ], []),
     (0.0, 1.0, 2.0,
      [(lt, "$trainer_help_message", 2),
        ],
      [(try_begin),
         (eq, "$trainer_help_message", 0),
         (tutorial_box, "str_trainer_help_1", "@Tutorial"),
       (else_try),
         (tutorial_box, "str_trainer_help_2", "@Tutorial"),
       (try_end),
       (val_add, "$trainer_help_message", 1),
          ]),

    ],
  ),
]
