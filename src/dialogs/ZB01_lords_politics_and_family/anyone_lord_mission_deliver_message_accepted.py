DIALOGS = [
[anyone, "lord_mission_deliver_message_accepted", [], "I appreciate it, {playername}. Here's the letter,\
 and a small sum to cover your travel expenses. Give my regards to {s13} when you see him.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_troop_add_gold", "trp_player", 30),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
    (assign, "$g_leave_encounter", 1),
   ]],
]
