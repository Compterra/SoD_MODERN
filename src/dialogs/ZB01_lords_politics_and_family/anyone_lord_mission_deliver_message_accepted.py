DIALOGS = [
[anyone, "lord_mission_deliver_message_accepted", [], "Here is the letter, {playername}, sealed and paid for the road.\
 Put it into {s13}'s hand, not merely into his hall, and let my regard travel with it.", "close_window",
   [(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
    (call_script, "script_troop_add_gold", "trp_player", 30),
    (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
    (assign, "$g_leave_encounter", 1),
   ]],
]
