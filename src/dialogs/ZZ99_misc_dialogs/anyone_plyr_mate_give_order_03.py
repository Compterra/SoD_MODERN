DIALOGS = [
[anyone|plyr, "mate_give_order", [], "Patrol this area", "mate_chat_pre_talk", [
    (party_set_ai_behavior, "$g_encountered_party", ai_bhvr_patrol_location),
    (party_get_position, pos1, "$g_encountered_party"),
    (party_set_ai_target_position, "$g_encountered_party", pos1),
	(call_script, "script_change_party_template", "$g_encountered_party", "pt_player_patrol_2"),
  ]],
]
