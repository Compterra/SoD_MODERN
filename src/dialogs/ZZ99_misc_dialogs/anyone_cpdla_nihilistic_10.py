DIALOGS = [
[anyone, "cpdla_nihilistic_10", [], "({s29} slowly breathes out and closes his eyes; you check his body and realize he has passed away. Perhaps now he's finally at rest.)", "close_window", [
	(call_script, "script_sod_runtime_trace_event", 5, "$g_enemy_party", "$g_talk_troop"),
	(call_script, "script_kill_kingdom_hero", "$g_talk_troop"),
	(call_script, "script_sod_safe_leave_encounter"),
	] ],
]
