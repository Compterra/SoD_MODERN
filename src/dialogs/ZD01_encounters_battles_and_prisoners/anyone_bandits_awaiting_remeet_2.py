DIALOGS = [
[anyone, "bandits_awaiting_remeet_2", [],
   "Oh, that business! Of course. Let us get down to it.", "close_window", [
     (assign, "$g_enemy_party", "$g_encountered_party"),
     (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
     (encounter_attack),
   ]],
]
