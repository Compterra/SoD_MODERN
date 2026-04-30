DIALOGS = [
[anyone, "convince_duel",
  [(troop_get_slot, ":troop_renown", "$g_talk_troop", slot_troop_renown),
    (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
	(val_div, ":troop_renown", 2),
	(lt, ":player_renown", ":troop_renown"),
	],
   "You think I would duel someone like you? Hah! Funny.", "convince_begin", []],
]
