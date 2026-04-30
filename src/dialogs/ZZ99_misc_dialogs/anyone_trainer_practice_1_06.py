DIALOGS = [
[anyone, "trainer_practice_1",
   [[eq, "$num_opponents_to_beat_in_a_row", 0], [eq, "$novice_training_difficulty", 3]],
 "It does my heart good to see such a promising talent. You have passed all tiers of training. You can now tell everyone that you have been trained by the master of the training field.",
   "novicemaster_finish_training",
   [[assign, "$num_opponents_to_beat_in_a_row", 3],
    [val_add, "$novice_training_difficulty", 1],
    [add_xp_to_troop, 300]]],
]
