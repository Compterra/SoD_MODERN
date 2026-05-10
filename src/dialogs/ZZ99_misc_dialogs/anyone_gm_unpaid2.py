DIALOGS = [
[anyone, "gm_unpaid2", [
  ], "You have had enough time, our pact is cancelled.", "close_window",[
  (call_script, "script_merc_player_end_guild_pact", "$g_talk_troop_faction", 0),
  (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", -5),
  (finish_mission),
  ]],
]
