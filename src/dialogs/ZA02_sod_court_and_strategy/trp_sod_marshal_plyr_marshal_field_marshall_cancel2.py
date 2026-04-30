DIALOGS = [
[trp_sod_marshal|plyr, "marshal_field_marshall_cancel2", [
  ], "Yes, cancel him.", "marshal_talk_again", [
	(faction_get_slot, ":cur_marshall", "fac_player_supporters_faction", slot_faction_marshall),
    (call_script, "script_change_player_relation_with_troop", ":cur_marshall", -10),
	(faction_set_slot, "fac_player_supporters_faction", slot_faction_marshall, 0),
	(call_script, "script_update_titles"),
  ]],
]
