DIALOGS = [
[trp_sod_marshal|plyr, "marshal_talk", [
	(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_marshall, 0),
	(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_marshall, -1),
  ], "I wish to cancel our kingdom's Field Marshall.", "marshal_field_marshall_cancel", []],
]
