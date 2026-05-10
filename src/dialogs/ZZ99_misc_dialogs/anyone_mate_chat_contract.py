DIALOGS = [
[anyone, "mate_chat_contract", [
    (party_get_slot,reg1,"$g_encountered_party",slot_party_merc_contract),
	(store_current_day, ":cur_day"),
	(val_sub, reg1, ":cur_day"),
    (val_max, reg1, 0),
    (call_script, "script_sod_external_party_describe_status_to_s20", "$g_encountered_party"),
   ], "Our writ has {reg1} days left. {s20}", "mate_chat_pre_talk", []],
]
