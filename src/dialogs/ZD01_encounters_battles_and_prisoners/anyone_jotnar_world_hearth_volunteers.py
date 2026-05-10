DIALOGS = [
[anyone, "jotnar_world_hearth_volunteers", [
   (eq, reg0, 1),
  ], "{reg1} Jotnar hearth fighter(s) step forward. They follow you for kin-right and winter memory, not coin alone.", "close_window", [
    (display_message, "@Jotnar hearth volunteers join your party.", 0x99CCFF),
    (assign, "$g_leave_encounter", 1),
  ]],
]
