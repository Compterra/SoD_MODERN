DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_bring_back_runaway_serfs")],
 "Well, some of the serfs working my fields in {s4} have run away. The ungrateful swine,\
 I let them plough my fields and rent my cottages, and this is how they repay me!\
 From what I've been hearing, they're running to {s3} as fast as they can,\
 and have split up into three groups to try and avoid capture.\
 I want you to capture all three groups and fetch them back to {s4} by whatever means necessary.\
 I should really have them hanged for attempting to escape, but we need hands for the upcoming harvest,\
 so I'll let them go off this time with a good beating.", "lord_mission_told",
   [
       (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
       (quest_get_slot, ":quest_object_center", "$random_quest_no", slot_quest_object_center),

       (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
       (str_store_party_name_link, s3, ":quest_target_center"),
       (str_store_party_name_link, s4, ":quest_object_center"),
       (setup_quest_text, "$random_quest_no"),
       (str_store_string, s2, "@{s9} asked you to catch the three groups of runaway serfs and bring them back to {s4} alive. He said that all three groups were heading toward {s3}."),
    ]],
]
