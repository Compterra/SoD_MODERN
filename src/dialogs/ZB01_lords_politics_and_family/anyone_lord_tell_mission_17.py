DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_capture_prisoners")],
 "A group of my soldiers were captured in a recent skirmish with the enemy.\
 Thankfully we have a mutual agreement of prisoner exchange, and they will release my men,\
 but they want us to give them prisoners of equal rank and number. Prisoners I don't currently have.\
 So, I need a good {man/warrior} to find me {reg1} {s3} as prisoners, that I may exchange them.", "lord_mission_told",
   [
       (quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
       (quest_get_slot, ":quest_target_amount", "qst_capture_prisoners", slot_quest_target_amount),
       (assign, reg1, ":quest_target_amount"),
       (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
       (str_store_troop_name_by_count, 3, ":quest_target_troop", ":quest_target_amount"),
       (setup_quest_text, "$random_quest_no"),
       (str_store_string, s2, "@{s9} has requested you to bring him {reg1} {s3} as prisoners."),
    ]],
]
