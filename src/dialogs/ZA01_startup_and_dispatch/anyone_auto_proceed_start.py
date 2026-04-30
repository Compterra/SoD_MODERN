DIALOGS = [
[anyone|auto_proceed, "start", [
		(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
		(this_or_next|is_between, "$g_talk_troop", "trp_knight_6_01", "trp_black_army_leader_1"),
		is_legate,
		(eq, "$g_talk_troop_faction", "fac_kingdom_6"),
		(eq, "$g_talk_troop_met", 0),
		(assign, "$centurion_first_meeting", 1),
		(assign, "$g_leave_encounter", 1),
	], "none", "centurion_personality", [] ],
]
