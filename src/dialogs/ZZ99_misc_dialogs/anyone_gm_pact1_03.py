DIALOGS = [
[anyone, "gm_pact1",[
	(store_current_day, ":cur_day"),
	(val_sub, ":cur_day", 30),
	(faction_get_slot, ":day", "$g_talk_troop_faction", slot_faction_pact_broken_day),
	(lt, ":cur_day", ":day"),
	], "Forget about it.", "gm_pretalk",[]],
]
