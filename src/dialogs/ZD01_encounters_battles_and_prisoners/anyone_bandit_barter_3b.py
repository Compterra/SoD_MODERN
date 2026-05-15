DIALOGS = [
[anyone, "bandit_barter_3b", [],
   "Then your purse was wiser than your mouth. Take {him/her}, lads, and leave the boots for later.", "close_window", [
     (assign, "$g_enemy_party", "$g_encountered_party"),
     (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
     (encounter_attack),
   ]],
]
