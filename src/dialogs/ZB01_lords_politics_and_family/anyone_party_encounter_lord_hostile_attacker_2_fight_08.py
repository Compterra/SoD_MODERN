DIALOGS = [
[anyone, "party_encounter_lord_hostile_attacker_2_fight", [
		(eq, "$g_talk_troop", "trp_kingdom_6_lord"),
	], "Then the time for talk is over. Come, {playername} ! Our battle will be one recorded in history !", "close_window", [
      (assign, "$g_enemy_party", "$g_encountered_party"),
      (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
      (encounter_attack),
    ] ],
]
