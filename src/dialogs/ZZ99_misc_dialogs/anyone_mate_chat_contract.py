DIALOGS = [
[anyone, "mate_chat_contract", [
    (party_get_slot,reg1,"$g_encountered_party",slot_party_merc_contract),
	(store_current_day, ":cur_day"),
	(val_sub, reg1, ":cur_day"),
   ], "{reg1} days.", "mate_chat_pre_talk", []],
]
