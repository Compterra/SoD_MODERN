MENUS = [
(
    "test_scene", mnf_auto_enter,
    "You enter the test scene.",
    "none",
    [],
    [

      ("enter", [], "Enter.", [[set_jump_mission, "mt_ai_training"], [jump_to_scene, "scn_test_scene"], [change_screen_mission]]),
      ("leave", [], "Leave.", [(leave_encounter), (change_screen_return)]),
    ]
  ),
]
