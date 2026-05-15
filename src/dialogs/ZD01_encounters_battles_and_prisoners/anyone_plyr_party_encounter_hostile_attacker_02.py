DIALOGS = [
[anyone|plyr, "party_encounter_hostile_attacker", [
                    ],
   "We will fight you to the end!", "close_window", [
     (assign, "$g_enemy_party", "$g_encountered_party"),
     (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
     (encounter_attack),
   ]],
]
