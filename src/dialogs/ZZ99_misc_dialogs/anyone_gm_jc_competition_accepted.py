DIALOGS = [
[anyone, "gm_jc_competition_accepted", [],
  "Great {playername}! The competition has already started. Go and find an opponent.", "gm_pretalk",[
	(call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
	(setup_quest_text, "$random_quest_no"),
    (str_store_string, s2, "@{s9} has invited you to a competition which has already begun in the jotnar Clan base."),
    (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
	]],
]
