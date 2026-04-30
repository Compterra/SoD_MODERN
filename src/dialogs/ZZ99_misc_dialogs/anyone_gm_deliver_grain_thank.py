DIALOGS = [
[anyone, "gm_deliver_grain_thank", [],
   "Thank you {playername},\
 We will never forget what you have done for us.", "gm_pretalk",
   [(quest_get_slot, ":quest_target_amount", "$g_gm_quest", slot_quest_target_amount),
	(quest_get_slot, ":quest_target_item", "$g_gm_quest", slot_quest_target_item),
    (troop_remove_items, "trp_player", ":quest_target_item", ":quest_target_amount"),
	(add_xp_as_reward, 500),
	(quest_get_slot, ":quest_revard", "$g_gm_quest", slot_quest_gold_reward),
	(troop_add_gold, "trp_player", ":quest_revard"),
    (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 6),
    (call_script, "script_succeed_quest", "$g_gm_quest"),
    (call_script, "script_end_quest", "$g_gm_quest"),
   ]],
]
