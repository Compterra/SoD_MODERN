DIALOGS = [
[anyone, "lord_report_to_army_completed", [], "Excellent. I will send the word when I have a task for you. For the moment, just follow us and stay close. We'll be moving soon.", "close_window", [
     (call_script, "script_end_quest", "qst_report_to_army"),
     (quest_set_slot, "qst_report_to_army", slot_quest_giver_troop, "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
     #Activating follow army quest
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (setup_quest_text, "qst_follow_army"),
     (str_store_string, s2, "@{s9} wants you to follow his army until further notice."),
     (call_script, "script_start_quest", "qst_follow_army", "$g_talk_troop"),
     (assign, "$g_player_follow_army_warnings", 0),
     (assign, "$g_leave_encounter", 1),
   ]],
]
