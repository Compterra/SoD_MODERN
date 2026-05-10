DIALOGS = [
[anyone|plyr, "cpdla_nihilistic_4", [(call_script, "script_change_player_honor", -5)], "I will leave you to rot here, like the scum you are. Move out, men ! We're finished here.", "close_window", [
	(call_script, "script_sod_runtime_trace_event", 5, "$g_enemy_party", "$g_talk_troop"),
	(call_script, "script_kill_kingdom_hero", "$g_talk_troop"),
	(call_script, "script_sod_safe_leave_encounter"),
	] ],
]
