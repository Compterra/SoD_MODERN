DIALOGS = [
[anyone, "party_encounter_lord_hostile_attacker_2_fight", [
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_respectful),
	], "So be it. All for the sake of the empire. Rally, soldiers ! Raise your weapons high ! Let Marsus crush our foes through the strength of our arms !", "close_window", [
      (assign, "$g_enemy_party", "$g_encountered_party"),
      (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
      (encounter_attack),
    ] ],
]
