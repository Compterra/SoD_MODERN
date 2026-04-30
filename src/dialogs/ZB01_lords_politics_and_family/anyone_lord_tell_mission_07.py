DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_hunt_down_fugitive")],
   "I have something you could help with, an issue with the lawless villain known as {s4}. \
 He murdered one of my men and has been on the run from his judgment ever since.\
 I can't let him get away with avoiding justice, so I've put a bounty of 300 denars on his head.\
 Friends of the murdered man reckon that this assassin may have taken refuge with his kinsmen at {s3}.\
 You might be able to hunt him down and give him what he deserves, and claim the bounty for yourself.", "lord_mission_hunt_down_fugitive_told",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, ":quest_target_dna", "$random_quest_no", slot_quest_target_dna),
     (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
     (str_store_party_name_link, s3, ":quest_target_center"),
     (call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
     (str_store_string, s4, s50),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s9} asked you to hunt down a fugitive named {s4}. He is believed to be at {s3}."),
   ]],
]
