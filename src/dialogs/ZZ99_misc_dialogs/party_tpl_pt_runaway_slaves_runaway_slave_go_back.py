DIALOGS = [
[party_tpl|pt_runaway_slaves, "runaway_slave_go_back", [(quest_get_slot, ":home_center", "qst_slavers_bring_back_runaway_slaves", slot_quest_target_center),
                                                       (str_store_party_name, s5, ":home_center")],
   "Then we go back to {s5}. Tell them we walked, not that we agreed.", "close_window",
   [
	(quest_get_slot, ":quest_object_center", "qst_slavers_bring_back_runaway_slaves", slot_quest_target_center),
	(party_set_ai_behavior, "$g_encountered_party", ai_bhvr_travel_to_party),
	(party_set_ai_object, "$g_encountered_party", ":quest_object_center"),
	(call_script, "script_sod_slavers_apply_player_action", sod_slaver_action_return_runaways, 2),
	(assign, "$g_leave_encounter", 1)]],
]
