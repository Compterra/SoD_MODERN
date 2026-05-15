DIALOGS = [
[anyone, "gm_jc_escort_accepted", [],
  "Great {playername}! Take her to {s13}.", "gm_pretalk",[
	(call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
	(quest_get_slot, ":target_center", "$random_quest_no", slot_quest_target_center),
	(str_store_party_name_link, s13, ":target_center"),
	(setup_quest_text, "$random_quest_no"),
	(party_add_members, "p_main_party", jotnar_clan_noble, 1),
    (str_store_string, s2, "@{s9} asked you to escort a Norn Mistress to {s13}."),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
	]],
]
