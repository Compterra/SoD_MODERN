DIALOGS = [
[anyone, "lord_start",[
	(eq, "$g_sod_convince_duel_paid", 0),
	(eq, "$g_sod_dueled_troop", "$g_talk_troop"),
	(eq, "$g_sod_convince_duel_won", 1),],
	"I must admit... You were better.", "convince_accept",[
	(assign, "$g_sod_convince_duel_paid", 1),
	(call_script, "script_sod_companion_apply_player_action", sod_companion_action_tournament_glory, 2),
	(call_script, "script_sod_companion_try_alayen_standard_incident", 2, 2),
	]],
]
