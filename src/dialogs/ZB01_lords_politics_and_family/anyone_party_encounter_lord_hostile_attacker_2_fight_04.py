DIALOGS = [
[anyone, "party_encounter_lord_hostile_attacker_2_fight", [
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_racist),
	], "In that case, there are no more options left but to slay you all. Very well. Throw yourselves against the might of the Imperial Legion, scum ! I will kill you first, and then scourge any other {s32} I can find ! Good riddance.", "close_window", [
      (assign, "$g_enemy_party", "$g_encountered_party"),
      (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
      (encounter_attack),
    ] ],
]
