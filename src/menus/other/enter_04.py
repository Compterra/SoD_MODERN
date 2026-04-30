MENUS = [
(
    "dhorak_keep", 0,
#    "Dhorak Keep, the stronghold of the bandits stands overlooking the barren wilderness.",
    "You enter Dhorak Keep. Its blackened walls loom over the barren waste, and the place feels less like a fortress than a lair waiting to swallow the unwary.",
    "none",
    [],
    [
      ("enter", [], "Pass beneath the gate.", [(set_jump_mission, "mt_town_center"), (jump_to_scene, "scn_dhorak_keep"), (change_screen_mission)]),
      ("leave", [], "Leave.", [(leave_encounter), (change_screen_return)]),
    ]
  ),
]
