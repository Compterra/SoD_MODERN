DIALOGS = [
[anyone, "troublesome_bandits_intro_2", [],
   "A bounty hunter! ... I hate bounty hunters! Kill {him/her}! Kill {him/her} now!", "close_window", [
     (assign, "$g_enemy_party", "$g_encountered_party"),
     (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
     (encounter_attack),
   ]],
]
