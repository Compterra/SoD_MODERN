DIALOGS = [
[anyone, "party_encounter_lord_hostile_attacker_2_fight", [
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_crusader),
	], "Hah ! Yes, nurture your frail hopes to the very end ! Then come and meet the judgement of our warrior god at the hands of his faithful crusaders ! It will be terrible to behold ! All who dies today, dies for Lord Marsus !", "close_window", [
      (assign, "$g_enemy_party", "$g_encountered_party"),
      (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
      (encounter_attack),
    ] ],
]
