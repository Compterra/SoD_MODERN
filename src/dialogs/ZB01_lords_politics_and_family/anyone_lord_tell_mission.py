DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_deliver_message")],
   "I need to send a letter to {s13} who should be currently at {s4}.\
 If you will be heading towards there, would you deliver it to him?\
 The letter needs to be in his hands in 30 days.", "lord_mission_deliver_message",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (call_script, "script_store_troop_name_link", s13, ":quest_target_troop"),
     (str_store_party_name_link, s4, ":quest_target_center"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to deliver a message to {s13}. {s13} was believed to be at {s4} when you were given this quest."),
   ]],
]
