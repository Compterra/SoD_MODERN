DIALOGS = [
[anyone, "lady_ask_for_quest", [(eq, "$random_quest_no", "qst_deliver_message_to_prisoner_lord")],
   "My poor {s17}, {s13}, is a prisoner in the {s14} dungeons.\
 The only way we can talk to each other is by exchanging letters whenever we can,\
 but the journey is so dangerous that we get little chance to do so.\
 Please, would you deliver one for me?", "lady_mission_told",
   [
     (quest_get_slot, ":quest_target_center", "$random_quest_no", slot_quest_target_center),
     (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),

     (try_begin),
       (troop_get_slot, ":cur_lord", "$g_talk_troop", slot_troop_spouse),
       (gt, ":cur_lord", 0),
       (str_store_string, s17, "str_husband"),
     (else_try),
       (str_store_string, s17, "str_father"),
     (try_end),

     (call_script, "script_store_troop_name", s11, "$g_talk_troop"),
     (call_script, "script_store_troop_name_link", s13, ":quest_target_troop"),
     (str_store_party_name_link, s14, ":quest_target_center"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@{s11} asked you to deliver a message to {s13}, who is imprisoned at {s14}."),
    ]],
]
