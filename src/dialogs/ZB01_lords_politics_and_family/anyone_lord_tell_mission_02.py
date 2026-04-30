DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_deliver_message_to_enemy_lord")],
   "I need to deliver a letter to {s13} of {s15}, who must be at {s4} currently.\
 If you are going towards there, would you deliver my letter to him? The letter needs to reach him in 40 days.", "lord_mission_deliver_message",
   [
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (call_script, "script_store_troop_name_link", s13, ":quest_target_troop"),
     (str_store_party_name_link, s4, ":quest_target_center"),
     (store_troop_faction, ":target_faction", ":quest_target_troop"),
     (str_store_faction_name_link, s15, ":target_faction"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to deliver a message to {s13} of {s15}. {s13} was believed to be at {s4} when you were given this quest."),
   ]],
]
