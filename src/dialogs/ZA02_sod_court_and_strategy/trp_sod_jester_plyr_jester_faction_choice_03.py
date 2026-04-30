DIALOGS = [
[trp_sod_jester|plyr, "jester_faction_choice", [], "Start wars between all kingdoms.", "jester_relations", [
	(try_for_range, ":kingdom_1", kingdoms_begin, kingdoms_end),
	(faction_slot_eq, ":kingdom_1", slot_faction_state, sfs_active),
	(try_for_range, ":kingdom_2", kingdoms_begin, kingdoms_end),
    (faction_slot_eq, ":kingdom_1", slot_faction_state, sfs_active),
	(neq, ":kingdom_1", ":kingdom_2"),
	(call_script, "script_diplomacy_start_war_between_kingdoms", ":kingdom_1", ":kingdom_2", 3),
    (val_add, "$g_sod_cheat_mode_used", 1),
	(try_end),	
	(try_end),
	]],
]
