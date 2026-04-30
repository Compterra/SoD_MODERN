DIALOGS = [
[anyone, "pretender_gm_message_delivered", [], "Oh? Let me see that...\
 Well well well! It was good of you to bring me this, {playername}. Take my seal as proof that I've received it.", "pretender_rebellion_cause_3", [
     (call_script, "script_succeed_quest", "$g_cur_deliver_quest"),
     (call_script, "script_end_quest", "$g_cur_deliver_quest"),
     (quest_get_slot, ":quest_giver", "$g_cur_deliver_quest", slot_quest_giver_troop),
	 (store_troop_faction, ":fac", ":quest_giver"),
     (call_script, "script_change_player_relation_with_faction", ":fac", 3),
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3),
	 (assign, "$g_cur_deliver_quest", -1),
   ]],
]
