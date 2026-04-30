SIMPLE_TRIGGERS = [
(24,[   (call_script, "script_add_merc_troops"),
		(call_script, "script_update_titles"),
		(call_script, "script_update_all_notes"),

        (try_for_range, ":gm", guild_masters_begin, guild_masters_end),
			(troop_set_slot, ":gm", slot_troop_daily_quest, 0),
			(troop_set_slot, ":gm", slot_troop_merc_bought, 0),
		(try_end),
		
		(try_for_range, ":gm", "trp_black_army_rep_1", "trp_slaver_deserter_1"),
			(troop_set_slot, ":gm", slot_troop_merc_bought, 0),
		(try_end),
		
		(store_sub, ":end", guilds_end, 1),
		(try_for_range, ":guild", guilds_begin, ":end"),
			(faction_slot_eq, ":guild", slot_faction_upgrade_permission, 1),
			(store_relation, ":rel", ":guild", "fac_player_supporters_faction"),
			(lt, ":rel", 10),
			(faction_set_slot, ":guild", slot_faction_upgrade_permission, 0),
			(str_store_faction_name, s13, ":guild"),
			(display_message, "@You lose your permission to promote {s13} troops.", red),
		(try_end),
			
		
		#bugfix
		(faction_get_slot, ":mercs", "fac_player_faction", slot_faction_merc_pact),
		(call_script, "script_merc_sync_player_guild_pact", ":mercs"),
		
		(store_random_in_range, "$g_sod_invasion_inaccuracy", 80, 121),
	   ]),
]
