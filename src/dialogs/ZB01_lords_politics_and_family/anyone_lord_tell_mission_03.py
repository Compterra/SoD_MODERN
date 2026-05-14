DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_escort_lady")],
   "There is a family matter, small in court and large in consequence. My {s17} {s13} is due for a visit to her relatives at {s14}.\
 The road has delayed her more than once, and this time she will not be delayed again.\
 I need a guard I can name without shame. Escort her to {s14}, {playername},\
 and see that she arrives with her dignity, baggage, and temper intact.", "lord_mission_told",
   [
     (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (try_begin),
       (troop_slot_eq, "$g_talk_troop", slot_troop_daughter, ":quest_object_troop"),
       (str_store_string, s17, "str_daughter"),
     (else_try),
       (str_store_string, s17, "str_wife"),
     (try_end),
     (call_script, "script_store_troop_name_link", s11, "$g_talk_troop"),
     (call_script, "script_store_troop_name_link", s13, ":quest_object_troop"),
     (str_store_party_name_link, s14, ":quest_target_center"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to escort {s13}, his {s17}, to {s14}."),
   ]],
]
