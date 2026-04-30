DIALOGS = [
[anyone|plyr, "gm_trusted_favor_confirm", [], "Do it. Call in the favor.", "gm_pretalk",[
   (call_script, "script_merc_apply_guild_master_favor", "$g_talk_troop_faction"),
]],
[anyone|plyr, "gm_trusted_favor_confirm", [], "Not now.", "gm_pretalk",[]],
]
