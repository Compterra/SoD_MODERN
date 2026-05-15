DIALOGS = [
[anyone, "party_encounter_lord_hostile_attacker_2_fight", [
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_capitalist),
	], "Answer violence by violence, right ? Fine by me. Imperial steel, that's my response ! Imperial steel, in the hands of my mercenaries ! Cry for your lives, peasants, they are over ! I'll make good money out of your weaponry, you won't be needing them anymore once we're finished !", "close_window", [
      (assign, "$g_enemy_party", "$g_encountered_party"),
      (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
      (encounter_attack),
    ] ],
]
