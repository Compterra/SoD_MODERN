DIALOGS = [
[anyone, "centurion_avoid_battle", [
	
	(try_begin),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_sane),
		(str_store_string, s68, "@(Sigh), that's a good excuse but I can't believe you, even if it's true. It's either your head, or mine. And I suppose we're both very attached to them. I can't help but repeat: surrender, or prepare for battle."),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_respectful),
		(str_store_string, s68, "@I concur, {playername}, but my orders are very explicit and come from the Legate himself. I cannot withdraw."),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_imperialist),
		(str_store_string, s68, "@I must give you credit for your care towards your people, but unfortunately I cannot let you evade me any further. My orders have been given, my objective is clear: to destroy or capture you. Make your choice."),
	(else_try),
		(troop_slot_eq, "$g_talk_troop", slot_troop_centurion_personality, slcp_racist),
		(str_store_string, s68, "@Your offerings leave me cold. If anything, you are lowering my already tiny respect towards you. Show some backbone, {playername} ! Your parents would weep if they saw how pathetic you are now ! Make your decision and deal with the consequences like a good ruler is supposed to !"),
	(else_try),
		(str_store_string, s68, "@That was a low blow, {playername}. Indeed, I'd prefer some other date for our clash but you need to realize there are forces out there which have already decided instead of us. There is no more place for arguing."),
	(try_end),
   ], "{s68}", "centurion_avoid_battle_denied", []],
]
