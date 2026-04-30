DIALOGS = [
[trp_jotnar_clan_norn_mistress, "event_triggered", [],
   "Thank you, {playername}. Go to Mistress Velandir to claim your reward. Farewell.", "close_window", [
   (call_script, "script_succeed_quest", "qst_jotnar_clan_escort"),
   (party_remove_members, "p_main_party", "trp_jotnar_clan_norn_mistress", 1),
   ]],
]
