DIALOGS = [
[anyone,     "prisoner_chat_release2", [], "Oh, thank you, {sir/madam}.  Blessings on you!", "close_window",
    [(remove_troops_from_prisoners, "$g_talk_troop", 1),
	(store_random_in_range, ":rand", 10, 200),  #twan453
	(store_character_level, ":troop_level", "$g_talk_troop"),
	(try_begin),
	(lt, ":rand", ":troop_level"),              #twan453 end
	(call_script, "script_change_player_honor", 1),
	(try_end),]],
]
