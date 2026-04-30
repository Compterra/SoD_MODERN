DIALOGS = [
[anyone, "gm_mission_deliver_message_accepted", [], "I appreciate it, {playername}. Here's the letter,\
 and a small sum to cover your travel expenses. Give my regards to {s13} when you see him.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_troop_add_gold", "trp_player", 50),
    (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 1),
    (assign, "$g_leave_encounter", 1),
	(quest_set_slot, "$random_quest_no", slot_quest_giver_troop, "$g_talk_troop"),
  (finish_mission),
   ]],
]
