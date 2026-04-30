DIALOGS = [
[anyone|plyr, "mate_give_order", [], "Follow me", "mate_chat_pre_talk", [
    (party_set_ai_object, "$g_encountered_party", "p_main_party"),
    (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_escort_party),
	(call_script, "script_change_party_template", "$g_encountered_party", "pt_player_patrol"),
  ]],
]
