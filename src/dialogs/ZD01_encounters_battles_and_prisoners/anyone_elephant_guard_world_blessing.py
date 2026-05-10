DIALOGS = [
[anyone, "elephant_guard_world_blessing", [
   (eq, reg0, 1),
  ], "Kneel, then rise. Elephant remembers those who shield the frightened. Your warriors will carry that memory into battle.", "close_window", [
    (display_message, "@The Elephant Guard blesses your company. Your party gains experience and their regard improves.", 0x8B4513),
    (assign, "$g_leave_encounter", 1),
  ]],
]
