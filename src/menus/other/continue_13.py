MENUS = [
(
    "siege_attack_meets_sally", 0,
    "The defenders sally out to meet your assault.",
    "none",
    [
    ],
    [
      ("continue", [],
       "Continue...",
       [
             (jump_to_menu, "mnu_battle_debrief"),
             (call_script, "script_sod_battle_commander_apply_before_mission"),
             (change_screen_mission),
       ]),
    ]
  ),
]
