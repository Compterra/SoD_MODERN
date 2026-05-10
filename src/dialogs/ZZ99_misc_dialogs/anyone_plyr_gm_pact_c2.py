DIALOGS = [
[anyone|plyr, "gm_pact_c2", [
   ], "Deal.", "gm_pact_c3",[
   (call_script, "script_sod_player_charge_gold", 500),
   (call_script, "script_merc_player_start_guild_pact", "$g_talk_troop_faction", 500),
   ]],
]
