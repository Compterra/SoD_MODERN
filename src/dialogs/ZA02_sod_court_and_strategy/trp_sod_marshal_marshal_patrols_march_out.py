DIALOGS = [
[trp_sod_marshal, "marshal_patrols_march_out", [],
    "Yes, sir!", "marshal_talk_again", [
	(try_for_parties, ":cur_party"),
		(call_script, "script_cf_is_patrol", ":cur_party"),
		(eq, reg0, 1),
		(party_get_attached_to, ":attached_center", ":cur_party"),
		(eq, ":attached_center", "$g_encountered_party"),
		(call_script, "script_party_set_ai_state", ":cur_party", spai_accompanying_army, "p_main_party"),
	(try_end),
	]
  ],
]
