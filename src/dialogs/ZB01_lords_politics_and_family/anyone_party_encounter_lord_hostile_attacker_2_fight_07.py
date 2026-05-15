DIALOGS = [
[anyone, "party_encounter_lord_hostile_attacker_2_fight", [
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_nihilistic),
	], "So much hate, so much noise... Let's bring it to a whole new level. Love the pain, relish the agony ! A feast of flesh, yeeess ! And once we're through with the bloodbath, I will craft puppets from your bones and gift them to children ! Such a happy ending ! HAHAHAHA !", "close_window", [
      (assign, "$g_enemy_party", "$g_encountered_party"),
      (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
      (encounter_attack),
    ] ],
]
