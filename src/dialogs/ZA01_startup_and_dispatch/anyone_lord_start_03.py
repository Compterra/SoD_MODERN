DIALOGS = [
[anyone, "lord_start",[
	(eq, "$g_sod_convince_duel_paid", 0),
	(eq, "$g_sod_dueled_troop", "$g_talk_troop"),
	(eq, "$g_sod_convince_duel_won", 0),
	],
	"We had a deal, now go and pay the debt with your own money.", "close_window",[
	(quest_set_slot,  "$g_convince_quest", slot_quest_current_state, 1),
	(assign, "$g_leave_encounter", 1),
    (call_script, "script_succeed_quest", "$g_convince_quest"),
	(assign, "$g_sod_convince_duel_paid", 1),
	]],
]
