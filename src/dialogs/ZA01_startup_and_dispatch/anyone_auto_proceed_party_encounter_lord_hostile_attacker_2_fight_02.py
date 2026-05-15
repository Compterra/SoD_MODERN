DIALOGS = [
[anyone, "party_encounter_lord_hostile_attacker_2_fight", [
	], "Then there is nothing more to say. Draw your steel, {playername}; we settle this on the field.", "close_window", [
      (assign, "$g_enemy_party", "$g_encountered_party"),
      (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
      (encounter_attack),
    ] ],
]
