DIALOGS = [
[anyone|plyr, "gm_pact_e4", [
   ], "Deal.", "gm_pact_e5",[
   (call_script, "script_sod_player_charge_gold", 1000),
   (call_script, "script_merc_player_start_guild_pact", "$g_talk_troop_faction", 1000),
   ]],
]
