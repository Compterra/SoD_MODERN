DIALOGS = [
[anyone, "lord_mission_told_scout_waypoints_accepted", [], "Good {man/lass}! Simply pass near {s13}, {s14} and {s15} and check out what's there. Make a note of anything you find and return to me as soon as possible.", "close_window",
   [
     (call_script, "script_end_quest", "qst_follow_army"),
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (str_store_party_name_link, s13, "$qst_scout_waypoints_wp_1"),
     (str_store_party_name_link, s14, "$qst_scout_waypoints_wp_2"),
     (str_store_party_name_link, s15, "$qst_scout_waypoints_wp_3"),
     (setup_quest_text, "$g_random_army_quest"),
     (str_store_string, s2, "@{s9} asked you to scout {s13}, {s14} and {s15}, then report back."),
     (call_script, "script_start_quest", "$g_random_army_quest", "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter", 1),
    ]],
]
