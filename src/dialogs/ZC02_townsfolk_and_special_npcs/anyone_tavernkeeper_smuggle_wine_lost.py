DIALOGS = [
[anyone, "tavernkeeper_smuggle_wine_lost", [], "What? I was waiting for that wine for weeks! And now you are telling me that you lost it? You may rest assured that I will let the Slavers know about this.", "close_window",
   [(add_xp_as_reward, 40),
    (faction_get_slot, ":plyr_debt", "fac_sod_merc_guild6", player_debt_to_faction),
	(val_add, ":plyr_debt", "$qst_slavers_deliver_wine_debt"),
	(faction_set_slot, "fac_sod_merc_guild6", player_debt_to_faction, ":plyr_debt"),
    (call_script, "script_fail_quest", "qst_slavers_deliver_wine"),
    (call_script, "script_end_quest", "qst_slavers_deliver_wine"),
   ]],
]
