DIALOGS = [
[anyone, "deserter_barter_3b", [],
   "Then we take our pay the ugly way. The slavers can argue over what is left.", "close_window", [
     (assign, "$g_enemy_party", "$g_encountered_party"),
     (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
     (encounter_attack),
   ]],
]
