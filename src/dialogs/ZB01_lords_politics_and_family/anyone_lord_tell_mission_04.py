DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_deal_with_bandits_at_lords_village")],
   "A group of bandits have taken refuge in my village of {s1}.\
 They are plundering nearby farms, and getting rich and fat stealing my taxes and feasting on my cattle.\
I'd like nothing better than to go out there and teach them a lesson,\
 but I have my hands full at the moment, so I can't do anything about it.", "lord_mission_deal_with_bandits_told",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (str_store_party_name_link, s15, ":quest_target_center"),
     (call_script, "script_store_troop_name_link", s13, "$g_talk_troop"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s13} asked you to drive the bandits out of the village of {s15} and report back."),
   ]],
]
