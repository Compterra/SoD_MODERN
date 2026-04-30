DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", training_gound_trainers_begin, training_gound_trainers_end),
                    (neq, "$waiting_for_training_fight_result", 0)],
 "Ha! Looks like you've developed a bit of a limp there. Don't worry, even losses have their value, provided you learn from them. Shake the stars out of your eyes and get back in there. There's no other way to win.", "trainer_practice_1",
   [(assign, "$num_opponents_to_beat_in_a_row", 3), (assign, "$waiting_for_training_fight_result", 0)]],
]
