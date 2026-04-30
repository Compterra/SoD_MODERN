MENUS = [
(
    "four_ways_inn", mnf_auto_enter,
    "You arrive at the Four Ways Inn. Warm lamplight spills from the shutters, and the smell of ale, woodsmoke, wet leather, and road dust hangs in the evening air.",
    "none",
    [],
    [

#      ("enter", [], "Enter.", [[set_jump_mission, "mt_town_default"], [jump_to_scene, "scn_conversation_scene"], [change_screen_mission]]),
      ("enter", [], "Push through the inn door.", [(set_jump_mission, "mt_camera_test"), (jump_to_scene, "scn_four_ways_inn"), (change_screen_mission)]),
      ("leave", [], "Leave.", [(leave_encounter), (change_screen_return)]),
    ]
  ),
]
