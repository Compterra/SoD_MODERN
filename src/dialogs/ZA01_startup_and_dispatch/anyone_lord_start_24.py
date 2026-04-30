DIALOGS = [
[anyone, "lord_start", [(store_partner_quest, ":lords_quest"),
                         (eq, ":lords_quest", "qst_scout_waypoints"),
                         (check_quest_succeeded, "qst_scout_waypoints"),
                         (str_store_party_name, s13, "$qst_scout_waypoints_wp_1"),
                         (str_store_party_name, s14, "$qst_scout_waypoints_wp_2"),
                         (str_store_party_name, s15, "$qst_scout_waypoints_wp_3"),
                         ],
   "You make a good scout, {playername}. My runner just brought me your reports of the mission to {s13}, {s14} and {s15}. Well done.", "lord_scout_waypoints_thank",
   [
     #TODO: Change reward
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (add_xp_as_reward, 100),
     (call_script, "script_end_quest", "qst_scout_waypoints"),
     #Reactivating follow army quest
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (setup_quest_text, "qst_follow_army"),
     (str_store_string, s2, "@Your mission is complete, {s9} wants you to resume following his army until further notice."),
     (call_script, "script_start_quest", "qst_follow_army", "$g_talk_troop"),
     (assign, "$g_player_follow_army_warnings", 0),
     ]],
]
