DIALOGS = [
[anyone|plyr, "gm_pact_cancel4",[
	], "So be it.", "close_window",[
  (faction_get_slot, ":debt", "$g_talk_troop_faction", player_debt_to_faction),
  (call_script, "script_merc_player_end_guild_pact", "$g_talk_troop_faction", 1),
  (try_begin),
    (gt, ":debt", 0),
    (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", -3),
  (try_end),
  (finish_mission),
	]],
]
