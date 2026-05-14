DIALOGS = [
[trp_sod_marshal, "marshal_field_marshall_elections", [
  ], "So I'll start the preparations.", "marshal_talk_again", [
	(faction_set_slot, "fac_player_supporters_faction", slot_faction_marshall, -1),
	(jump_to_menu, "mnu_sod_marshall_selection"),
	(finish_mission),
	]],
]
