DIALOGS = [
[anyone, "elephant_guard_world_volunteers", [
   (eq, reg0, 1),
  ], "{reg1} shrine-road warrior(s) step forward. They will follow you while your path still serves life more than plunder.", "close_window", [
    (display_message, "@Elephant Guard volunteers join your party.", 0x8B4513),
    (assign, "$g_leave_encounter", 1),
  ]],
]
