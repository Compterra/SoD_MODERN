DIALOGS = [
[anyone, "lord_tell_mission", [(eq, "$random_quest_no", "qst_lend_companion")],
 "I don't have a job for you right now, but your companion {s3} is a skilled {reg3?lass:fellow}\
 and I need someone with {reg3?her:his} talents. Will you lend {reg3?her:him} to me for a while?", "lord_tell_mission_lend_companion",
   [
       (quest_get_slot, ":quest_target_troop", "$random_quest_no", slot_quest_target_troop),
       (quest_get_slot, ":quest_target_amount", "$random_quest_no", slot_quest_target_amount),
       (val_add, ":quest_target_amount", 1),
       (assign, reg1, ":quest_target_amount"),
       (call_script, "script_store_troop_name_link", s9, "$g_talk_troop"),
       (call_script, "script_store_troop_name", s3, ":quest_target_troop"),
       (setup_quest_text, "$random_quest_no"),
       (troop_get_type, reg3, ":quest_target_troop"),
       (str_store_string, s2, "@{s9} asked you to lend your companion {s3} to him for a week."),
    ]],
]
