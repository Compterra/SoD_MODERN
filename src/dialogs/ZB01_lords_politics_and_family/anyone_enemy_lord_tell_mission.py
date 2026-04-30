DIALOGS = [
[anyone, "enemy_lord_tell_mission", [(eq, "$random_quest_no", "qst_lend_surgeon")],
   "I have a friend here, an old warrior, who is very sick. Pestilence has infected an old battle wound,\
 and unless he is seen to by a surgeon soon,  he will surely die. This man is dear to me, {playername},\
 but he's also stubborn as a hog and refuses to have anyone look at his injury because he doesn't trust the physicians here.\
 I have heard that you've a capable surgeon with you. If you would let your surgeon come here and have a look,\
 {reg3?she:he} may be able to convince him to give his consent to an operation.\
 Please, I will be deeply indebted to you if you grant me this request.", "lord_mission_told",
   [
     (quest_get_slot, ":quest_object_troop", "$random_quest_no", slot_quest_object_troop),
     (call_script, "script_store_troop_name_link", 1, "$g_talk_troop"),
     (call_script, "script_store_troop_name", 3, ":quest_object_troop"),
     (troop_get_type, reg3, ":quest_object_troop"),
     (setup_quest_text, "$random_quest_no"),
     (str_store_string, s2, "@Lend your experienced surgeon {s3} to {s1}."),
   ]],
]
