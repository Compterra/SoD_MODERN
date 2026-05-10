DIALOGS = [
[anyone, "jotnar_world_hearth_free_captives", [
   (eq, reg0, 1),
  ], "{reg1} captive(s) are taken into the hearth-ring. The clan gives them names, food, and witnesses. You gain {reg2} honor.", "close_window", [
    (display_message, "@The Jotnar shelter the freed captives.", 0x99CCFF),
    (assign, "$g_leave_encounter", 1),
  ]],
]
