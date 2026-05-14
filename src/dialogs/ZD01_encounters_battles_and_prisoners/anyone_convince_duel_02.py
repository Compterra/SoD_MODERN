DIALOGS = [
[anyone, "convince_duel",
   [(call_script, "script_cf_sod_valid_lord_duel_target", "$g_talk_troop")],
   "All right, let's fight.", "close_window",
   [
   (assign, "$g_leave_encounter", 1),
   (jump_to_menu, "mnu_convince_duel"),
   (finish_mission),
	]],
]
