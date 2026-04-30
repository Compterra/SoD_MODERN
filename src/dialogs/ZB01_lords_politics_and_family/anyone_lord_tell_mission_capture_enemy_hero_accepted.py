DIALOGS = [
[anyone, "lord_tell_mission_capture_enemy_hero_accepted", [],
   "I like your spirit! Go and bring me one of our enemies,\
 and I'll toast your name in my hall when you return! And reward you for your efforts, of course...", "close_window",
   [
     (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
     (call_script, "script_store_troop_name_link", s11, "$g_talk_troop"),
     (str_store_faction_name_link, s13, ":quest_target_faction"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to capture a lord from {s13}, any lord, and then drag your victim back to {s11} for safekeeping."),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     #TODO: Change this value
     (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
     (assign, "$g_leave_encounter", 1),
   ]],
]
