DIALOGS = [
[trp_sod_jester|plyr|repeat_for_parties, "jester_cheat_fief_choice", 
	[ (this_or_next|eq, "$cheat_mode", 1),
	(eq, "$g_sod_cheat_mode", 1),
	(store_repeat_object, ":party_no"),
	(is_between, ":party_no", walled_centers_begin, walled_centers_end),
	(neg|party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
	(str_store_party_name, s1, ":party_no")
	], "{s1}.", "jester_cheat_fief", [
	(store_repeat_object, ":party_no"),
    (call_script, "script_give_center_to_faction", ":party_no", "fac_player_supporters_faction"),
	(try_begin),
	(party_slot_eq, ":party_no", slot_party_type, spt_castle),
	(val_add, "$g_sod_cheat_mode_used", 10),
	(else_try),
	(val_add, "$g_sod_cheat_mode_used", 20),
	(try_end),
	(call_script, "script_give_center_to_lord", ":party_no", "trp_player", 0),
	]],
]
