DIALOGS = [
[anyone|auto_proceed, "gm_quest_ask", [], "A task?", "gm_tell_mission",
   [
	(try_begin),
	   (troop_slot_eq, "$g_talk_troop", slot_troop_daily_quest, 0),
	   (call_script, "script_get_random_quest", "$g_talk_troop"),
	   (assign, "$random_quest_no", reg0),
	   (troop_set_slot, "$g_talk_troop", slot_troop_daily_quest, 1),
	(else_try),
	   (assign, "$random_quest_no", -1),
	(try_end),
	(try_begin),
	    (eq, "$g_sod_cheat_mode", 1),
	    (troop_set_slot, "$g_talk_troop", slot_troop_daily_quest, 0),
	(try_end),
   ]],
]
