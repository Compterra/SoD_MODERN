DIALOGS = [
[anyone, "gm_raise_troops_thank", [],
   "Thank you {playername},\
 We will never forget what you have done for us.", "gm_pretalk",
   [(quest_get_slot, ":quest_target_troop", "$g_gm_quest", slot_quest_target_troop),
	(quest_get_slot, ":quest_target_amount", "$g_gm_quest", slot_quest_target_amount),
	(call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 8),
	(party_remove_members, "p_main_party", ":quest_target_troop", ":quest_target_amount"),
	(call_script, "script_succeed_quest", "$g_gm_quest"),
	(call_script, "script_end_quest", "$g_gm_quest"),
	(troop_add_gold, "trp_player", 500),
	]],
]
