DIALOGS = [
[anyone|plyr, "cpdla_nihilistic_2", [], "Yes. I believe it is. Your wound is deep, and you lost much blood.", "close_window", [
	(call_script, "script_sod_runtime_trace_event", 5, "$g_enemy_party", "$g_talk_troop"),
	(call_script, "script_kill_kingdom_hero", "$g_talk_troop"),
	(call_script, "script_sod_safe_leave_encounter"),
	(display_message, "@The Centurion slowly breathes out and falls still. The Legion has lost another commander.", 0xCC9966),
	] ],
]
