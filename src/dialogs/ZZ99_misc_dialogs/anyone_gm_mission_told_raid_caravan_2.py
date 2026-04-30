DIALOGS = [
[anyone, "gm_mission_told_raid_caravan_2", [(quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
                                                            (str_store_faction_name_link, s13, ":quest_target_faction")],
   "I will be grateful to you.", "close_window", [
   (quest_get_slot, ":quest_target_faction", "$random_quest_no", slot_quest_target_faction),
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (str_store_faction_name_link, s13, ":quest_target_faction"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to raid a caravan of {s13}."),
     (call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
     (call_script, "script_change_player_relation_with_faction", "$g_talk_troop_faction", 2),
     (assign, "$g_leave_encounter", 1),
  (finish_mission),]],
]
