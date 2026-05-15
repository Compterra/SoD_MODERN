DIALOGS = [
[anyone, "bandit_barter", [],
   "Hey, I've heard of you! You slaughter us freebooters like dogs, and now you expect us to let you go for a few stinking coins? Forget it. You gave us no quarter, and you'll get none from us.", "close_window", [
     (assign, "$g_enemy_party", "$g_encountered_party"),
     (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
     (encounter_attack),
   ]],
]
