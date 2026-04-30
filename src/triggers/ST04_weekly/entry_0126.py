SIMPLE_TRIGGERS = [
(24*7, [
	 (try_for_range, ":cur_guild", guilds_begin, "fac_sod_merc_guild6"),
		(assign, ":employed", 0),
		(try_for_range, ":employer", kingdoms_begin, kingdoms_end),
			(faction_slot_eq, ":employer", slot_faction_merc_pact, ":cur_guild"),
			(try_begin),
				(faction_slot_eq, ":employer", slot_faction_state, sfs_active),
				(assign, ":employed", 1),
			(else_try),
				(faction_set_slot, ":employer", slot_faction_merc_pact, 0),
			(try_end),
		(try_end),
		(eq, ":employed", 0),
		(call_script, "script_cf_merc_guild_give_new_employer", ":cur_guild"),
	 (try_end),
	 (call_script, "script_update_all_notes"),
  
	 (faction_get_slot, ":mercenaries", "fac_player_faction", slot_faction_merc_pact),
	 (gt, ":mercenaries", 0),
	 (jump_to_menu, "mnu_mercenaries_weekly_payment"),
	 ]),
]
