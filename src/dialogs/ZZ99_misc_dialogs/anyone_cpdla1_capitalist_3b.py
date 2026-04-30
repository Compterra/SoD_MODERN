DIALOGS = [
[anyone, "cpdla1_capitalist_3b", [
	(troop_set_slot, "$g_talk_troop", slot_troop_prisoner_of_party, "p_main_party"),
     (party_force_add_prisoners, "p_main_party", "$g_talk_troop", 1), #take prisoner
	 (neg|troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_sane),
	 (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -30),
     (call_script, "script_change_player_relation_with_faction_ex", "$g_talk_troop_faction", -3),
     (call_script, "script_event_hero_taken_prisoner_by_player", "$g_talk_troop"),
     (call_script, "script_add_log_entry", logent_lord_captured_by_player, "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction"),
	], "No ! NO ! Anything but that ! I can't stand such a punishment ! I beg you ! Please... 3000 Denars ? O- or if you accompany me to the nearest town, I can make it more ! 5000 ! 10000 ! ANYTHING !", "cpdla1_capitalist_4b", [] ],
]
