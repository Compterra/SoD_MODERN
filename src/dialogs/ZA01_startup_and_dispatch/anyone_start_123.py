DIALOGS = [
[anyone, "start", [(is_between, "$g_talk_troop", training_gound_trainers_begin, training_gound_trainers_end),
                   (neq, "$waiting_for_training_fight_result", 0),
                   (neq, "$training_fight_won", 0)],
 "That was a good fight. ", "trainer_practice_1",
  [(val_sub, "$num_opponents_to_beat_in_a_row", 1),
   (assign, "$waiting_for_training_fight_result", 0),
   ]],
]
