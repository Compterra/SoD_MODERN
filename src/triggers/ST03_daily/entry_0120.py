SIMPLE_TRIGGERS = [
(24,
	[
	(try_for_parties, ":cur_party"),
		(party_slot_eq, ":cur_party", slot_party_type, spt_ai_mercenaries),
		(store_current_day, ":cur_day"),
		(party_get_slot,":time",":cur_party",slot_party_merc_contract),
		(val_sub, ":time", ":cur_day"),
		(lt, ":time", 0),
		(call_script, "script_merc_party_change_state", ":cur_party"),
	(try_end),
	]),
]
