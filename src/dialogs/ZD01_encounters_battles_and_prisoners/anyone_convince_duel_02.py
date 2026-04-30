DIALOGS = [
[anyone, "convince_duel",
   [],
   "All right, let's fight.", "close_window",
   [
   (assign, "$g_leave_encounter", 1),
   (finish_mission),
   (jump_to_menu, "mnu_convince_duel"),
	]],
]
