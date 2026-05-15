DIALOGS = [
[anyone|plyr, "centurion_avoid_battle_denied", [
	(try_begin),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_sane),
		(str_store_string, s68, "@Then there are no more options left but senseless slaughter. Fine by me..."),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_respectful),
		(str_store_string, s68, "@I see. Then I'll make my stand here. We'll fight to the last man if necessary."),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_imperialist),
		(str_store_string, s68, "@Then witness the iron resolve of the {s32} refugees ! Attack !"),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_racist),
		(str_store_string, s68, "@I have decided. I'll fight tooth and nail ! Come at me ! Your doom awaits !"),
	(else_try),
		(str_store_string, s68, "@Very well. No more arguing. Only death. We'll fight to the last drop of blood !"),
	(try_end),
   ], "{s68}", "close_window", [
      (assign, "$g_enemy_party", "$g_encountered_party"),
      (call_script, "script_let_nearby_parties_join_current_battle", 0, 0),
      (encounter_attack),
   ]],
]
