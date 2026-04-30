MISSION_TEMPLATES = [
(
    "camera_test", 0, -1,
    "camera Test.",
    [
#     (0, mtef_attackers, 0, aif_start_alarmed, 5, []),
     ],
    [
      (1, 0, 0, [(mission_cam_set_mode, 1),
          (entry_point_get_position, pos3, 3),
          (mission_cam_set_position, pos3)], []),
#      (ti_before_mission_start, 0, 0, [], [(set_rain, 1, 100)]),
      (ti_tab_pressed, 0, 0, [],
       [(finish_mission, 0)]),
    ],
  ),
]
