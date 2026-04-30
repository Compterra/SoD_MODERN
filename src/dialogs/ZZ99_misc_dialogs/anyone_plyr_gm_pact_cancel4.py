DIALOGS = [
[anyone|plyr, "gm_pact_cancel4",[
	], "So be it.", "close_window",[
  (call_script, "script_merc_player_end_guild_pact", "$g_talk_troop_faction", 1),
  (finish_mission),
	]],
]
