DIALOGS = [
[anyone, "elephant_guard_world_free_slaves", [
   (eq, reg0, 1),
  ], "{reg1} captive(s) are taken from your ranks and given road food, water, and witnesses. Elephant remembers mercy better than coin.", "close_window", [
    (display_message, "@You freed {reg1} captive(s). Honor rises by {reg2}, and the Elephant Guard approves.", 0x8B4513),
    (assign, "$g_leave_encounter", 1),
  ]],
]
