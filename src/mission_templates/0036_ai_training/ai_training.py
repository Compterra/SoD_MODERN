MISSION_TEMPLATES = [
(
    "ai_training", 0, -1,
    "You start training.",
    [
#     (0, 0, af_override_horse, aif_start_alarmed, 1, []),
     (0, 0, 0, aif_start_alarmed, 30, []),
#     (1, mtef_no_leader, 0, 0|aif_start_alarmed, 5, []),
#     (0, mtef_no_leader, 0, 0|aif_start_alarmed, 0, []),
#     (3, mtef_enemy_party|mtef_reverse_order, 0, aif_start_alarmed, 6, []),
#     (4, mtef_enemy_party|mtef_reverse_order, 0, aif_start_alarmed, 0, []),
     ],
    [
#      (ti_before_mission_start, 0, 0, [], [(set_rain, 1, 100)]),
      (ti_tab_pressed, 0, 0, [],
       [(finish_mission, 0)]),

      (0, 0, ti_once, [], [(assign, "$g_presentation_battle_active", 0),
                           ]),

      common_battle_order_panel,
      common_battle_order_panel_tick,
    ],
  ),
]
