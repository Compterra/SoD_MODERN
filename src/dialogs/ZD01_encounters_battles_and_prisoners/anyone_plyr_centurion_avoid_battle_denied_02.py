DIALOGS = [
[anyone|plyr, "centurion_avoid_battle_denied", [
	(try_begin),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_sane),
		(str_store_string, s68, "@No more choices left then... I give up. For now, that is."),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_respectful),
		(str_store_string, s68, "@Then I have few choices left. My army is unprepared for battle. I'll surrender."),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_imperialist),
		(str_store_string, s68, "@I won't sacrifice my subjects in vain. I give up."),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_racist),
		(str_store_string, s68, "@For the lives of my subjects, I'll bear the burden of defeat. I surrender."),
	(else_try),
		(str_store_string, s68, "@I surrender... for now, that is. The war is not yet over."),
	(try_end),
   ], "{s68}", "close_window", [(assign, "$g_player_surrenders", 1)]],
]
