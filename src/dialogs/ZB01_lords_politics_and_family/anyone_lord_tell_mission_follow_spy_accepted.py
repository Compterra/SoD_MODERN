DIALOGS = [
[anyone, "lord_tell_mission_follow_spy_accepted", [],
   "Good, I'm sure you'll do a fine job of it. One of my men will point the spy out to you when he leaves,\
 so you will know the man to follow. Remember, I want them both, and I want them alive.", "close_window",
   [
     (call_script, "script_store_troop_name_link", s11, "$g_talk_troop"),
     (str_store_party_name_link, s12, "$g_encountered_party"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to follow the spy that will leave {s12}. Be careful not to let the spy see you on the way, or he may get suspicious and turn back. Once the spy meets with his accomplice, you are to capture them and bring them back to {s11}."),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),

     (spawn_around_party, "p_main_party", "pt_spy_partners"),
     (assign, "$qst_follow_spy_spy_partners_party", reg0),
     (party_set_position, "$qst_follow_spy_spy_partners_party", pos63),
     (party_set_ai_behavior, "$qst_follow_spy_spy_partners_party", ai_bhvr_hold),
     (party_set_flags, "$qst_follow_spy_spy_partners_party", pf_default_behavior, 0),
     (set_spawn_radius, 0),
     (spawn_around_party, "$g_encountered_party", "pt_spy"),
     (assign, "$qst_follow_spy_spy_party", reg0),
     (party_set_ai_behavior, "$qst_follow_spy_spy_party", ai_bhvr_travel_to_party),
     (party_set_ai_object, "$qst_follow_spy_spy_party", "$qst_follow_spy_spy_partners_party"),
     (party_set_flags, "$qst_follow_spy_spy_party", pf_default_behavior, 0),
     (assign, "$g_leave_town", 1),
     (rest_for_hours, 2, 4, 0),
     #no need to set g_leave_encounter to 1 since this quest can only be given at a town
   ]],
]
