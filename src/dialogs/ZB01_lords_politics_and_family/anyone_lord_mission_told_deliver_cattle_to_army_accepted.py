DIALOGS = [
[anyone, "lord_mission_told_deliver_cattle_to_army_accepted", [], "Good. An army can march on courage for one day and beef for the rest. Bring those cattle before hunger starts giving orders.", "close_window",
   [
     (call_script, "script_end_quest", "qst_follow_army"),
     (quest_get_slot, ":quest_target_amount", "$g_random_army_quest", slot_quest_target_amount),
     (call_script, "script_store_troop_name_link", s13, "$g_talk_troop"),
     (assign, reg3, ":quest_target_amount"),
     (setup_quest_text, "$g_random_army_quest"),
     (str_store_string, s2, "@{s13} asked you to gather {reg3} heads of cattle and deliver them back to him."),
     (call_script, "script_start_quest", "$g_random_army_quest", "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter", 1),
    ]],
]
