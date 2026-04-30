SCRIPTS = [
("setup_talk_info",
    [
	  (try_begin),
		(store_troop_faction, ":guild", "$g_talk_troop"),
		(this_or_next|is_between, "$g_talk_troop", guild_masters_begin, guild_masters_end),
		(faction_slot_eq, ":guild", slot_guild_representative, "$g_talk_troop"),
		(store_relation, ":rel", "fac_player_faction", ":guild"),
		(assign, "$g_talk_troop_relation", ":rel"),
	  (try_end),
	  
      (talk_info_set_relation_bar, "$g_talk_troop_relation"),
      (call_script, "script_store_troop_name", s61, "$g_talk_troop"),
      (str_store_string, s61, "@ {s61}"),
      (assign, reg1, "$g_talk_troop_relation"),
      (str_store_string, s62, "str_relation_reg1"),
      (talk_info_set_line, 0, s61),
      (talk_info_set_line, 1, s62),
      (call_script, "script_describe_troop_relation", s63, "$g_talk_troop_relation"),
      (talk_info_set_line, 3, s63),
  ]),
]
